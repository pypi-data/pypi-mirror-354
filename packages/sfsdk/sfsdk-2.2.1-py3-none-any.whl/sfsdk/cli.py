#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

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


import argparse
import json
import os
import argcomplete, argparse
import re
import shlex
import docker
import sys
import time

from sfsdk import containers, imgsettings, log, utils

base_dir = os.path.expanduser('~/sf')

def img_snapshot(name, new_name, force):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not new_name:
        new_name = imgsettings.get_snapshot_name(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    if new_name in imgsettings.settings.get('images', {}).keys():
        raise log.FatalMsg('Image %s already exists' % new_name)

    current_container_conf = imgsettings.get_container_conf(name)

    if containers.container_status(current_container_conf['name']) != 'running':
        raise log.FatalMsg("""Image is not running, consider running 'sfsdk img-watch %s' before running img-snapshot again.""" % (name))

    additional_paths = []

    paths_file = os.path.join(image_settings['build_dir'], '.sfsdk-watch.txt')

    additional_paths = []
    try:
        with open(paths_file, 'r') as stream:
            additional_paths = [ l for l in stream.read().split('\n') if l ]
    except OSError:
        log.debug("Error reading %s" % (paths_file))
        log.warn("Can't find result from img-watch, consider running 'sfsdk img-watch %s' before running img-snapshot again." % (name))

    monitored_paths = []

    # Add additional paths without duplicates
    for additional_path in additional_paths:
        if not (additional_path in monitored_paths or additional_path + '/' in monitored_paths):
            monitored_paths.append(additional_path)

    container_settings = { v['name']:v['default'] for v in imgsettings.get_settings(new_name) }

    imgsettings.add_image_settings(
            new_name,
            build_dir = None,
            from_dir = image_settings['build_dir'],
            container_settings = container_settings
            )

    new_img_settings = imgsettings.settings.get('images', {}).get(new_name)
    new_build_dir = new_img_settings['build_dir']

    containers.save_container_snapshot(
            container_name = current_container_conf['name'],
            snapshot_folder = new_build_dir,
            modified_paths = monitored_paths
        )

    if monitored_paths:
        log.block("""The following paths have been exported from the running container and applied over the build folder.:

%s

The new project image has been saved as %s.
""" % (
            '\n'.join(monitored_paths),
            new_name
            )
        )

def img_add(name, build_dir, from_dir):

    # Docker image name limitations
    if not re.match('[a-z0-9][a-z0-9_.-]*$', name):
        raise log.FatalMsg('Image name is not valid')

    container_settings = { v['name']:v['default'] for v in imgsettings.get_settings(name) }

    imgsettings.add_image_settings(
            name,
            build_dir = build_dir,
            from_dir = from_dir,
            container_settings = container_settings
            )

    image_settings = imgsettings.settings.get('images', {}).get(name)

    log.success("""New image %s has been added at '%s'""" % (name, utils.prettypath(image_settings['build_dir'])))

def img_build(name, source):
    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add %s' to add it" % (name, name))

    log.info('Building exercise image %s...' % name)
    build_generator = containers.build_image(image_settings['build_dir'], name)

    built = False
    error = None

    for line in build_generator:
        if 'stream' in line:
            output = line['stream'].strip('\n')
            log.block(output, end='\n', prefix='')

            if output.startswith('Successfully built'):
                built = True

        if 'error' in line:
            error = line['error']

    if built:
        log.success("Build complete")
    else:
        raise log.FatalMsg("The build of the image failed: %s" % error)

def img_shell(name, command):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    container_settings = imgsettings.get_container_conf(name)
    container_name = container_settings['name']

    os.execvp("docker", [ "docker", "exec", "-it", container_name ] + shlex.split(command))

def img_run(name, force, exercise_name = None, flag_name = None):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    containers.run_tool_pre_img_container_conf(base_dir, image_settings['build_dir'])

    container_settings = imgsettings.get_container_conf(name)
    container_name = container_settings['name']

    container_exists = containers.container_exists(container_name)
    container_status = containers.container_status(container_name)

    if container_exists and not force:
        if container_status == 'running':
            raise log.FatalMsg("Container %s is already running, you can stop and rebuild it." % container_name)
        else:
            raise log.FatalMsg("Container %s is not running, run 'sfsdk img-run %s --force' to delete and re-run" % (container_name, name))

    data = [
            [ "Container name:", container_name ],
            [ "RDP port:", '127.0.0.1:%s' % image_settings['container']['external_rdp_port'] ],
            [ "RDP credentials:", 'sf:' + image_settings['container']['rdp_password']  ],
            [ "Application port:", '127.0.0.1:%s' % image_settings['container']['external_http_port'] ]
        ]

    if flag_name:
        container_settings['environment']['EXERCISE'] = imgsettings.generate_exercise_environment(flag_name)
        data.append(
            [ "Flag name:", flag_name ]
        )
    else:
        data.append(
            [ "Exercise name:", 'none' ]
        )        

    if container_status != None:
        containers.container_remove(container_name)

    containers.run_container(container_settings)

    log.success("Container %s has been started" % container_name)
        

    log.tablify(data)


def img_stop(names):

    image_names = imgsettings.resolve_images(names)

    for name in image_names:

        image_settings = imgsettings.settings.get('images', {}).get(name)
        
        if names[0] != "all":
            containers.run_tool_post_img_container_conf(base_dir, image_settings['build_dir'])

        if not image_settings:
            raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

        container_settings = imgsettings.get_container_conf(name)
        container_name = container_settings['name']

        container_was_running = (containers.container_status(container_name) != 'running')

        if not container_was_running:

            if not containers.container_remove(container_name):
                log.warn("Container %s is not running" % container_name)
            else:
                log.success("Container %s has been stopped" % container_name)

def img_watch(name, folder, count):

    image_settings = imgsettings.settings.get('images', {}).get(name)

    if not image_settings:
        raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

    output_file = os.path.join(image_settings['build_dir'], '.sfsdk-watch.txt')
    
    container_settings = imgsettings.get_container_conf(name)

    container_name = container_settings['name']
    log.debug("Writing img-watch output to %s" % output_file)
    log.success("Please wait, preparing %s to run img-watch.." % (container_name))

    containers.watch_container(container_name, watch_folder = folder)
    last_json_output = []

    try:

        i = 0
        found = 0

        while True:

            if count == 0:
                pass
            elif i > count:
                break
            else:
                i+=1

            exit_code, output = containers.exec_on_container(
                    container_name,
                    'cat /tmp/sfsdkwatch.json',
                    )

            if exit_code == 0 and output:

                found += 1
                if found == 1:
                    log.success("Started watching changes in %s folder.." % (folder))


                try:
                    json_output = json.loads(output)
                except json.JSONDecodeError as e:
                    continue

                if sorted(json_output) != sorted(last_json_output):
                    last_json_output = json_output[:]

                    log.success("%s Changed files and folders:" % (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

                    directory_list = '\n'.join(last_json_output)
                    log.block(directory_list, end='\n\n')

                    with open(output_file, 'w+') as stream:
                        stream.write(directory_list)

            time.sleep(1)

    except KeyboardInterrupt:
        pass

def img_ls():

    data = [ ]

    for image_name, image_data in imgsettings.settings['images'].items():

        img_running = (containers.container_status(image_data['container']['container_name']) == 'running')

        data.append([
            image_name,
            'Yes' if img_running else 'No',
            image_data['container']['container_name'] if img_running else '',
            image_data['container']['external_rdp_port'] if img_running else '',
            'sf:' + image_data['container']['rdp_password'] if img_running else '',
            image_data['container']['external_http_port'] if img_running else '',
            ]
        )

    log.tablify(
            data,
            header = [
                'Name',
                'Running',
                'Container name',
                'RDP port',
                'RDP creds',
                'Application port'
            ]
        )

def img_rm(names):

    image_names = imgsettings.resolve_images(names)

    for name in image_names:

        image_settings = imgsettings.settings.get('images', {}).get(name)

        if not image_settings:
            raise log.FatalMsg("Image %s does not exist, run 'sfsdk img-add' to add it" % name)

        try:
            imgsettings.remove_image(name)
        except log.FatalMsg as e:
            log.warn(str(e))
        else:
            log.success("Image %s data has been removed" % name)

def _get_argparser():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    parser_add = subparsers.add_parser('img-add', help='Add new image')
    parser_add.add_argument(
        '-b', '--build-dir', dest='build_dir', help='Build folder')
    parser_add.add_argument(
        '-i', '--import-build', dest='from_dir', help='Import build directory')
    parser_add.add_argument('name', help='New image name')

    parser_ls = subparsers.add_parser('img-ls', help='List images')

    parser_build = subparsers.add_parser('img-build', help='Build an image')
    parser_build.add_argument('name', help='Image to build')
    parser_build.add_argument(
            '--source', dest='source', help='Source name')

    parser_run = subparsers.add_parser('img-run', help='Run last build')
    parser_run.add_argument('name', help='Project to run')
    parser_run.add_argument('-f', '--force', dest='force', help='Remove previous containers', action='store_true')
    parser_run.add_argument(
        '--flag-name', '-fn', dest='flag_name', help='Pass flag name'
        )
        
    parser_stop = subparsers.add_parser('img-stop', help='Stop running image')
    parser_stop.add_argument('names', nargs='+', help='Images names (or "all")')

    parser_shell = subparsers.add_parser('img-shell', help='Interact with a running image')
    parser_shell.add_argument('name', help='Run interactive shell on a running image')
    parser_shell.add_argument('-c', '--command', help='Command to execute', default='/bin/bash')

    parser_watch = subparsers.add_parser('img-watch', help='Keep track of the fs changes on a running image')
    parser_watch.add_argument(
        '-f', '--folder', dest='folder', help='Folder to watch', default='/home/sf')
    parser_watch.add_argument(
        '-c', '--count', dest='count', help=argparse.SUPPRESS, default=0, type=int)
    parser_watch.add_argument('name', help='Running image to watch')

    snapshot = subparsers.add_parser('img-snapshot', help='Save the current state as new')
    snapshot.add_argument(
        '--new-name', dest='new_name', help='The new image name')
    snapshot.add_argument(
        '-f', '--force', dest='force', help='Overwrite the export directory', action='store_true')
    snapshot.add_argument('name', help='Running image to snapshot')

    parser_rm = subparsers.add_parser('img-rm', help='Remove local image')
    parser_rm.add_argument('names', nargs='+', help='Images names')

    parser.add_argument(
        '--verbose', '-v', dest='verbose', help='Verbose', action='store_true')

    return parser

def cli():

    parser = _get_argparser()

    argcomplete.autocomplete(parser, always_complete_options=False)
    kwargs = vars(parser.parse_args())

    if not kwargs.get('subparser'):
        parser.print_help()
        raise log.FatalMsg()

    imgsettings.load(base_dir)

    # Initialize docker client
    containers.load()

    # Set verbose and remove from arguments
    if kwargs['verbose']:
        log.set_verbose()

    del kwargs['verbose']

    globals()[kwargs.pop('subparser').replace('-', '_')](**kwargs)


def main():
    try:
        cli()
    except log.FatalMsg as e:
        msg = str(e)
        if msg: 
            log.warn(str(e))
        sys.exit(1)
    except KeyboardInterrupt as e:
        print('')
