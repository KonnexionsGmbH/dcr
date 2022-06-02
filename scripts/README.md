# DCR - File Directory **`scripts`**

This directory contains the following shell scripts for Unix and Windows systems:

- `run_prep_bash_scripts.sh`: to configure EOL and execution rights of shell scripts in Unix systems.
- `run_setup_postgresql`: to download an [official PostgreSQL Docker](https://hub.docker.com/_/postgres) image and create a Docker container suitable for **DCR** from it..

The subdirectory `0.9.3` contains the following scripts:

`run_install_4_vm_wsl2_1.sh` and
`run_install_4_vm_wsl2_2.sh`

These two scripts install the necessary tools for development and operation in an Ubuntu 20.04 LTS environment as an alternative.
Ubuntu can be provided either native, via a virtual machine or via the WSL2 (Windows Subsystem for Linux).
If Ubuntu runs under WSL2, the installation of Docker Desktop is not necessary - Docker Desktop must then be installed in Windows 10.
The first script expects the following input parameter:

- `HOST_ENVIRONMENT` - input `vm`(default value) or `wsl2`

Before script `run_install_4_vm_wsl2_2.sh` is executed, the current terminal window must be closed and a new one opened.
For WSL2, the integration of the Ubuntu distro must also be switched on in Docker Desktop (`Settings` / `Resources` / `WSL INTEGRATION`).  