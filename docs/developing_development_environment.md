# DCR - Developing - Development Environment

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

To set up a suitable development environment under **`Ubuntu 20.04 LTS`**, on the one hand a suitable ready-made Docker image is provided and on the other hand two scripts to create the development system in a standalone system, a virtual environment or the **`Windows Subsystem for Linux (WSL2)`** are available.

### 1. Docker Image

The ready-made Docker images are available on [DockerHub](https://hub.docker.com){:target="_blank"} under the following link:

[dcr_dev - Document Content Recognition Development Image](https://hub.docker.com/repository/docker/konnexionsgmbh/dcr_dev){:target="_blank"}

When selecting the Docker image, care must be taken to select the appropriate version of the Docker image.

### 2. Script-based Solution

Alternatively, for a **`Ubuntu 20.04 LTS`** environment that is as unspoiled as possible, the following two scripts are available in the **`scripts`** file directory:

- **`scripts/0.9.1/run_install_4-vm_wsl2_1.sh`**
- **`scripts/0.9.1/run_install_4-vm_wsl2_2.sh`**

After a **`cd scripts`** command in a terminal window, the script **`run_install_4-vm_wsl2_1.sh`** must first be executed. 
Administration rights (**`sudo`**) are required for this. 
Afterwards, the second script **`run_install_4-vm_wsl2_2.sh`** must be executed in a new terminal window.
