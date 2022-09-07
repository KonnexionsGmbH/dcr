#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_install_4_vm_wsl2_2.sh: Install a dcr_dev environment for Ubuntu 20.04 - Step 2.
#
# ------------------------------------------------------------------------------

export PWD_PREVIOUS="${PWD}"
cd ${HOME}

echo " "
echo "Script $0 is now running"

export LOG_FILE=run_install_4_vm_wsl2_2.log

echo " "
echo "You can find the run log in the file ${LOG_FILE}"
echo " "

exec &> >(tee -i ${LOG_FILE}) 2>&1
sleep .1

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "Install a dcr_dev environment for Ubuntu 20.04 - Step 2."
echo "------------------------------------------------------------------------------"
echo "HOST_ENVIRONMENT                  : ${HOST_ENVIRONMENT}"
echo "USER                              : ${USER}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="
echo "Step: Install asdf - part 2"
echo "------------------------------------------------------------------------------"
echo " "
echo "Current version of asdf is: $(asdf --version)"
echo " "
echo "=============================================================================="

sudo rm -rf ${HOME}/.asdf/downloads/python
sudo rm -rf ${HOME}/.asdf/downloads/tmux

sudo rm -rf ${HOME}/.asdf/installs/python
sudo rm -rf ${HOME}/.asdf/installs/tmux

sudo rm -rf ${HOME}/.asdf/plugins/python
sudo rm -rf ${HOME}/.asdf/plugins/tmux

echo "------------------------------------------------------------------------------"
echo "Step: Install Python3 - Version ${VERSION_PYTHON3}"
echo "------------------------------------------------------------------------------"
asdf plugin add python
asdf install python ${VERSION_PYTHON3}
asdf global python ${VERSION_PYTHON3}
echo "------------------------------------------------------------------------------"
echo "Step: Install pip"
echo "------------------------------------------------------------------------------"
wget --quiet --no-check-certificate -nv https://bootstrap.pypa.io/get-pip.py
python3 -m pip install --upgrade pip
sudo rm -f get-pip.py
echo " "
echo "=============================================================================> Version  Python3: "
echo " "
echo "Current version of Python3: $(python3 --version)"
echo " "
echo "Current version of pip: $(pip --version)"
echo " "
echo "=============================================================================="

echo "------------------------------------------------------------------------------"
echo "Step: Install tmux - Version ${VERSION_TMUX}"
echo "------------------------------------------------------------------------------"
asdf plugin add tmux
asdf install tmux ${VERSION_TMUX}
asdf global tmux ${VERSION_TMUX}
echo " "
echo "=============================================================================> Version  tmux: "
echo " "
echo "Current version of tmux: $(tmux -V)"
echo " "
echo "=============================================================================="

if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    echo "------------------------------------------------------------------------------"
    echo "Step: Install DBeaver - Version ${VERSION_DBEAVER}"
    echo "------------------------------------------------------------------------------"
    wget --quiet https://github.com/dbeaver/dbeaver/releases/download/${VERSION_DBEAVER}/dbeaver-ce-${VERSION_DBEAVER}-linux.gtk.x86_64.tar.gz
    sudo tar -xf dbeaver-ce-${VERSION_DBEAVER}-linux.gtk.x86_64.tar.gz
    sudo rm -rf ${HOME_DBEAVER}
    sudo cp -r dbeaver ${HOME_DBEAVER}
    sudo rm -rf dbeaver
    sudo rm -f dbeaver-ce-*.tar.gz
    echo " "
    echo "=============================================================================> Version  DBeaver: "
    echo " "
    echo "Current version of DBeaver: $(${HOME_DBEAVER}/dbeaver -help)"
    echo " "
    echo "=============================================================================="
fi

echo "------------------------------------------------------------------------------"
echo "Step: Cleanup"
echo "------------------------------------------------------------------------------"
sudo apt-get -qy autoremove
sudo rm -rf /tmp/*

cd "${PWD_PREVIOUS}"

echo "=============================================================================> Current Date: "
echo " "
date
echo " "
# Show Environment Variables -------------------------------------------------------
echo "=============================================================================> Environment variable LANG: "
echo " "
echo "${LANG}"
echo " "
echo "=============================================================================> Environment variable LANGUAGE: "
echo " "
echo "${LANGUAGE}"
echo " "
echo "=============================================================================> Environment variable LC_ALL: "
echo " "
echo "${LC_ALL}"
echo " "
echo "=============================================================================> Environment variable PATH: "
echo " "
echo "${PATH}"
echo " "
# Show component versions ----------------------------------------------------------
echo "=============================================================================> Components"
( /bin/bash ${HOME}/kxn_install/run_version_check.sh )
echo " "
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="

exit 0
