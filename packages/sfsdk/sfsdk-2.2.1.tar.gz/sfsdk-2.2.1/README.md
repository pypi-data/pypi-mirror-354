This repository is part of the SecureFlag Platform.

Please refer to the official [documentation](https://community.secureflag.com/) for installation instructions and further information.

## Build Tests

### Prerequisites

Install `qemu binfmt-support qemu-user-static` on an x86 based system.

Such as with apt `sudo apt-get install qemu binfmt-support qemu-user-static`

### Run tests

To run isolated docker test installs for various versions of linux and platforms AMD64/ARM64 use:

```bash
./tests/docker-build/test-all-build.sh
```
