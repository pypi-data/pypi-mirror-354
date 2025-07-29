# This file is part of the SecureFlag Platform.
# Copyright (c) 2024 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sfsdk import log, utils, imgsettings
import docker
import time
import tempfile
import tarfile
import os
import json
import io
import subprocess
import sys
import requests

dockerc = None

dockerfile_data = """
FROM secureflag/sf-community

COPY fs/ /
RUN chown -R sf:sf /home/sf
""".lstrip()


class ContainerExec(object):

    def __init__(self, client, id, output):
        self.client = client
        self.id = id
        self.output = output

    def inspect(self):
        return self.client.api.exec_inspect(self.id)

    def poll(self):
        return self.inspect()['ExitCode']

    def communicate(self, line_prefix=b''):
        
        for data in self.output:
            if not data: continue
            offset = 0
            while offset < len(data):
                sys.stdout.buffer.write(line_prefix)
                nl = data.find(b'\n', offset)
                if nl >= 0:
                    slice = data[offset:nl+1]
                    offset = nl+1
                else:
                    slice = data[offset:]
                    offset += len(slice)
                sys.stdout.buffer.write(slice)

            sys.stdout.flush()

        while self.poll() is None:
            raise RuntimeError('Hm could that really happen?')
        
        return self.poll()


def load():

    global dockerc

    dockerc = docker.from_env()

    try:
        dockerc.info()
    except Exception as e:
        log.debug(str(e))
        raise log.FatalMsg("Error, can't communicate with the Docker daemon")

def image_exists(image_name):

    try:
        dockerc.images.get(image_name)
    except docker.errors.ImageNotFound as _:
        return False
    else:
        return True

def tag_image(image_name, tag):

    dockerc.images.get(image_name).tag(tag)

def run_tool_script(base_dir, build_dir, script_name, settings_loader):
    script_path = os.path.join(build_dir, 'tools', script_name)

    if os.path.isfile(script_path):
        log.info(f"Executing {script_name}")

        result = subprocess.run(
            [script_path], 
            stderr=sys.stderr,
            stdout=sys.stdout
        )

        if result.returncode != 0:
            raise log.FatalMsg(f"Script {script_name} exited with non-zero status.")

        settings_loader(base_dir)

def run_tool_pre_img_container_conf(base_dir, build_dir):
    run_tool_script(base_dir, build_dir, 'pre-img-run.sh', imgsettings.load)

def run_tool_post_img_container_conf(base_dir, build_dir):
    run_tool_script(base_dir, build_dir, 'post-img-run.sh', imgsettings.load)

def run_tool_pre_test_container_conf(base_dir, build_dir):
    run_tool_script(base_dir, build_dir, 'pre-test-run.sh', imgsettings.load)

def run_tool_post_test_container_conf(base_dir, build_dir):
    run_tool_script(base_dir, build_dir, 'post-test-run.sh', imgsettings.load)

def run_container(conf):

    global containers

    conf['detach'] = True
    try:
        dockerc.containers.run(**conf)
    except docker.errors.ImageNotFound as e:
        raise log.FatalMsg("Image has not been built yet, run 'sfsdk img-build %s' and retry" % conf['image'])
    except docker.errors.ContainerError as e:
        raise log.FatalMsg('A container named %s already exists' % conf['name'])
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def containers_list():

    try:
         return [ c.name for c in dockerc.containers.list() ]
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def container_exists(container_name):

    try:
        dockerc.containers.get(container_name)
    except (docker.errors.NotFound, requests.exceptions.ChunkedEncodingError) as e:
        return False
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    return True


def container_status(container_name):

    try:
        return dockerc.containers.get(container_name).status
    except (docker.errors.NotFound, requests.exceptions.ChunkedEncodingError) as e:
        pass
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def container_remove(container_name):

    try:
        container = dockerc.containers.get(container_name)
        container.stop(timeout=20)
        container.remove(force=True)
    except (docker.errors.NotFound, requests.exceptions.ChunkedEncodingError) as e:
        return False
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    return True

def wait_until_running(container_name, delay = 1, count = 10):

    for i in range(count):

        try:
            container = dockerc.containers.get(container_name)
        except (docker.errors.NotFound, requests.exceptions.ChunkedEncodingError) as e:
            pass
        except docker.errors.APIError as e:
            raise log.FatalMsg(e.explanation)

        if container.status == 'running':
            return

        time.sleep(1)

    raise log.FatalMsg("Container failed running in %d seconds" % (delay*count))

def upload_paths(container_name, paths, dest):

    try:

        container = dockerc.containers.get(container_name)
        tar_buffer = tar_from_paths(paths)
        container.put_archive(dest, tar_buffer.tobytes())

    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def exec_stream_on_container(container_name, cmd, stdout=True, stderr=True, stdin=False,
                    tty=False, privileged=False, user='', detach=False,
                    socket=False, environment=None, workdir=None):

    """ Helper to allow streaming container execution, that also provides exit code"""

    container = dockerc.containers.get(container_name)

    exec_id = container.client.api.exec_create(
        container.id, cmd, stdout=stdout, stderr=stderr, stdin=stdin, tty=tty,
        privileged=privileged, user=user, environment=environment,
        workdir=workdir)['Id']

    output = container.client.api.exec_start(
        exec_id, detach=detach, tty=tty, stream=True, socket=socket)

    return ContainerExec(container.client, exec_id, output)


def exec_on_container(container_name, cmd, tty = True):

    try:
        container = dockerc.containers.get(container_name)

        exit_code, output = container.exec_run(
                cmd,
                stdout = True,
                tty = tty
                )

        return exit_code, output.decode("utf-8", errors="ignore").rstrip("\r\n")

    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)


def watch_container(container_name, watch_folder = '/home/sf', status_json = '/tmp/sfsdkwatch.json'):
            
    try:
        container = dockerc.containers.get(container_name)

        if container.exec_run(
                "ls /tmp/sfsdkwatch.py"
                ).exit_code != 0:
            upload_paths(container_name,
                    [ os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "sfsdkwatch.py"
                    ) ], '/tmp')

        _, pgrep_output = container.exec_run(
                "pgrep -f '/usr/bin/python3 /tmp/sfsdkwatch.py'",
                stdout = True
                )

        if not pgrep_output:
            if container.exec_run(
                    "/usr/bin/python3 -c 'import watchdog'"
                    ).exit_code != 0:
                if container.exec_run("sh -c \
                        'apt-get update && \
                        apt-get install -y python3-watchdog'",
                        environment = [ "DEBIAN_FRONTEND=noninteractive" ]).exit_code != 0:
                    raise log.FatalMsg("Error installing python-watchdog, check if internet is enabled")

            container.exec_run(
                "/usr/bin/python3 /tmp/sfsdkwatch.py '%s' '%s'" % (watch_folder, status_json), 
                detach = True
                )
    except docker.errors.NotFound:
        raise log.FatalMsg("Container is not running, start it with 'sfsdk run <image-name>' and retry")
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def get_watched_paths(container_name):

    try:
        container = dockerc.containers.get(container_name)

        if container.exec_run(
                "ls /tmp/sfsdkwatch.json"
                ).exit_code != 0:
            return {}
        
        watch_data = container.exec_run("cat /tmp/sfsdkwatch.json").output
        
        if not watch_data:
            return {}
        else:
            return json.loads(watch_data)
    except ValueError as e:
        raise log.FatalMsg('Error reading the modified files')
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

def tar_from_paths(paths):

    tarstream = io.BytesIO()
    with tarfile.TarFile(fileobj=tarstream, mode='w') as t:

        for path in paths:
            abs_path = os.path.abspath(path)
            t.add(abs_path, arcname=os.path.basename(path), recursive=True)

    tarstream.flush()
    return tarstream.getbuffer()

def tar_from_bytes(data):
    f = io.BytesIO()

    for chunk in data:
        f.write(chunk)

    f.seek(0)

    return tarfile.open(fileobj=f)

def is_empty_folder(snapshot_folder):

    if not os.path.isdir(snapshot_folder):
        os.makedirs(snapshot_folder)
        
    if [ x for x in os.listdir(snapshot_folder) if x != '.keep' ]:
        return False

    return True

def generate_dockerfile(build_folder, modified_paths = []):

    with open(
            os.path.join(build_folder, 'Dockerfile'),
            'w'
            ) as dockerfile:

        dockerfile.write(dockerfile_data)

def create_snapshot(snapshot_folder, snapshot_tmp, modified_paths):

    dest_home = os.path.join(snapshot_folder, 'fs/home/sf')
    
    utils.merge_tree(
        os.path.join(snapshot_tmp, 'sf'), 
        dest_home,
        preserve_symlinks = True,
    )

def extract_modified_from_tar(tar_file, modified_paths):

    snapshot_tmp = tempfile.mkdtemp(prefix='sdk.snapshot.')

    members_to_extract = []
    for m in tar_file.getmembers():
        file_path = os.path.join('/home', m.name)

        # Standardize output using an ending / if folders.
        if m.isdir():
            file_path = os.path.join(file_path, '')

        # Extract everything starts with modified_paths
        if any((mp for mp in modified_paths + [ '/home/sf/exercise' ] if file_path.startswith(mp) and not m in [n.name for n in members_to_extract])):
            members_to_extract.append(m)

    tar_file.extractall(path=snapshot_tmp, members=members_to_extract)

    return snapshot_tmp

def save_container_snapshot(container_name, snapshot_folder, modified_paths):

    try:
        container = dockerc.containers.get(container_name)
    except (docker.errors.NotFound, requests.exceptions.ChunkedEncodingError) as e:
        raise log.FatalMsg("Can't find container %s" % container_name)
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    try:
        tar_data, _ = container.get_archive('/home/sf')
    except Exception as e:
        log.debug(str(e))
        raise log.FatalMsg("Error pulling data from container")

    tar_file = tar_from_bytes(tar_data)

    try:
        snapshot_tmp = extract_modified_from_tar(
            tar_file, 
            modified_paths
        )
    except Exception as e:
        log.debug(str(e))
        raise log.FatalMsg("Error extracting data from container")

    create_snapshot(snapshot_folder, snapshot_tmp, modified_paths)

def build_image(exercise_path, image_name):

    try:
        return dockerc.api.build(
                path=exercise_path,
                tag=image_name,
                decode=True,
                buildargs={'DEV_BUILD': 'true'}
                )
    except docker.errors.APIError as e:
        log.warn("Error building %s from %s" % (image_name, exercise_path))
        raise log.FatalMsg(e.explanation)

def image_remove(image_name):

    try:
        dockerc.images.remove(image_name, force=True)
    except (docker.errors.NotFound, requests.exceptions.ChunkedEncodingError) as e:
        return False
    except docker.errors.APIError as e:
        raise log.FatalMsg(e.explanation)

    return True