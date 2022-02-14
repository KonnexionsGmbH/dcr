#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_install_4_vm_wsl2_1.sh: Install a dcr_dev environment for Ubuntu 20.04 - Step 1.
#
# ----------------------------------------------------------------------------------

sudo rm -rf /tmp/*

export HOST_ENVIRONMENT_DEFAULT=vm

export CURRENT_PATH=$(pwd)

export VERSION_DCR_DEV=0.5.0

export VERSION_DBEAVER=21.3.4
export VERSION_HTOP=3.1.2
export VERSION_PANDOC=2.17.1.1
export VERSION_PYTHON3=3.10.2
export VERSION_TMUX=3.2a

if [ -z "$1" ]; then
    echo "=============================================================================="
    echo "vm   - Virtual Machine"
    echo "wsl2 - Windows Subsystem for Linux Version 2"
    echo "------------------------------------------------------------------------------"
    read -rp "Enter the underlying host environment type [default: ${HOST_ENVIRONMENT_DEFAULT}] " HOST_ENVIRONMENT
    export HOST_ENVIRONMENT=${HOST_ENVIRONMENT}

    if [ -z "${HOST_ENVIRONMENT}" ]; then
    export HOST_ENVIRONMENT=${HOST_ENVIRONMENT_DEFAULT}
    fi
else
    export HOST_ENVIRONMENT=$1
fi

mkdir -p ${HOME}/kxn_install
rm -rf ${HOME}/kxn_install/*

cp -r ../../../scripts/run_version_check.sh ${HOME}/kxn_install

cd ${HOME}

# Setting Environment Variables ----------------------------------------------------
export DEBIAN_FRONTEND=noninteractive
export LOCALE=en_US.UTF-8

PATH_ADD_ON=
PATH_ORIG=${PATH_ORIG}

if [ -z "${PATH_ORIG}" ]; then
    PATH_ORIG=\"${PATH}\"
else
    PATH_ORIG=\"${PATH_ORIG}\"
fi

export TIMEZONE=Europe/Zurich

echo '' >> ${HOME}/.bashrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.bashrc
echo '# Environment dcr_dev for Ubuntu 20.04 - Start' >> ${HOME}/.bashrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.bashrc
echo " "
echo "Script $0 is now running"

export LOG_FILE=run_install_4_vm_wsl2_1.log

echo ""
echo "You can find the run log in the file ${LOG_FILE}"
echo ""

exec &> >(tee -i ${LOG_FILE}) 2>&1
sleep .1

echo "=============================================================================="
echo "Start $0"
echo "------------------------------------------------------------------------------"
echo "Install a dcr_dev environment for Ubuntu 20.04 - Step 1."
echo "------------------------------------------------------------------------------"
echo "HOST_ENVIRONMENT                  : ${HOST_ENVIRONMENT}"
echo "USER                              : ${USER}"
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=============================================================================="
echo "Supplement necessary system software"
echo "------------------------------------------------------------------------------"
sudo apt-get clean -qy

sudo apt-get update -qy
sudo apt-get install -qy gnupg

sudo apt-get update -qy
sudo apt-get upgrade -qy

sudo apt-get install -qy autoconf \
                         byacc \
                         curl \
                         dos2unix \
                         git \
                         libbz2-dev \
                         libffi-dev \
                         liblzma-dev \
                         libncurses-dev \
                         libncurses5-dev \
                         libncursesw5-dev \
                         libpoppler-dev \
                         libreadline-dev \
                         libsqlite3-dev \
                         libssl-dev \
                         libxml2-dev \
                         libxmlsec1-dev \
                         llvm \
                         locales \
                         lsb-release \
                         pkg-config \
                         procps \
                         tk-dev \
                         tzdata \
                         unzip \
                         vim \
                         wget \
                         xz-utils \
                         zlib1g-dev

echo "------------------------------------------------------------------------------"
echo "Step: Setting Locale & Timezone"
echo "------------------------------------------------------------------------------"
sudo ln -fs /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
sudo dpkg-reconfigure --frontend noninteractive tzdata
sudo locale-gen "${LOCALE}"
sudo update-locale "LANG=de_CH.UTF-8 UTF-8"
sudo locale-gen --purge "de_CH.UTF-8"
sudo dpkg-reconfigure --frontend noninteractive locales

echo "------------------------------------------------------------------------------"
echo "Step: Setting up the environment: 1. Setting the environment variables"
echo "------------------------------------------------------------------------------"

# from asdf ------------------------------------------------------------------------
PATH_ADD_ON=${HOME}/.asdf/bin:${HOME}/.asdf/shims:${PATH_ADD_ON}
if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    # from DBeaver ---------------------------------------------------------------------
    export HOME_DBEAVER=/opt/dbeaver
    PATH_ADD_ON=${HOME_DBEAVER}:${PATH_ADD_ON}
fi

# from Python 3 --------------------------------------------------------------------
PATH_ADD_ON=${HOME}/.asdf/installs/python/${VERSION_PYTHON3}/bin:${PATH_ADD_ON}

# from Locale & Timezone -----------------------------------------------------------
echo '' >> ${HOME}/.bashrc
eval echo 'export DEBIAN_FRONTEND=${DEBIAN_FRONTEND}' >> ${HOME}/.bashrc
eval echo 'export HOST_ENVIRONMENT=${HOST_ENVIRONMENT}' >> ${HOME}/.bashrc
eval echo 'export LANG=${LOCALE}' >> ${HOME}/.bashrc
eval echo 'export LANGUAGE=${LOCALE}' >> ${HOME}/.bashrc
eval echo 'export LC_ALL=${LOCALE}' >> ${HOME}/.bashrc
eval echo 'export LOCALE=${LOCALE}' >> ${HOME}/.bashrc

echo '' >> ${HOME}/.bashrc
eval echo 'export VERSION_DCR_DEV=${VERSION_DCR_DEV}' >> ${HOME}/.bashrc

echo '' >> ${HOME}/.bashrc
if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    eval echo 'export VERSION_DBEAVER=${VERSION_DBEAVER}' >> ${HOME}/.bashrc
fi
eval echo 'export VERSION_HTOP=${VERSION_HTOP}' >> ${HOME}/.bashrc
eval echo 'export VERSION_PYTHON3=${VERSION_PYTHON3}' >> ${HOME}/.bashrc
eval echo 'export VERSION_TMUX=${VERSION_TMUX}' >> ${HOME}/.bashrc

echo "------------------------------------------------------------------------------"
echo "Step: Setting up the environment: 2. Initializing the interactive shell session"
echo "------------------------------------------------------------------------------"
echo '' >> ${HOME}/.bashrc
echo 'alias python=python3' >> ${HOME}/.bashrc
echo 'alias vi=vim' >> ${HOME}/.bashrc

# PATH variable --------------------------------------------------------------------
echo '' >> ${HOME}/.bashrc
if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    # from DBeaver ---------------------------------------------------------------------
    eval echo 'export HOME_DBEAVER=${HOME_DBEAVER}' >> ${HOME}/.bashrc
fi

eval echo 'export PATH=${PATH_ORIG}:${PATH_ADD_ON}' >> ${HOME}/.bashrc
eval echo 'export PATH_ORIG=${PATH_ORIG}' >> ${HOME}/.bashrc

# from asdf ------------------------------------------------------------------------
echo '' >> ${HOME}/.bashrc
eval echo '. ${HOME}/.asdf/asdf.sh' >> ${HOME}/.bashrc
eval echo '. ${HOME}/.asdf/completions/asdf.bash' >> ${HOME}/.bashrc

echo '' >> ${HOME}/.bashrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.bashrc
echo '# Environment dcr_dev for Ubuntu 20.04 - End' >> ${HOME}/.bashrc
echo '# ----------------------------------------------------------------------------' >> ${HOME}/.bashrc

# Initializing the interactive shell session ---------------------------------------
source ${HOME}/.bashrc

echo "------------------------------------------------------------------------------"
echo "Step: Install asdf - part 1"
echo "------------------------------------------------------------------------------"
sudo rm -rf ${HOME}/.asdf
git clone https://github.com/asdf-vm/asdf.git ${HOME}/.asdf
echo "=============================================================================="

echo "------------------------------------------------------------------------------"
echo "Step: Install htop - Version ${VERSION_HTOP}"
echo "------------------------------------------------------------------------------"
wget --no-check-certificate -nv https://github.com/htop-dev/htop/archive/${VERSION_HTOP}.tar.gz
sudo tar -zxf ${VERSION_HTOP}.tar.gz
sudo rm -rf htop
sudo mv htop-${VERSION_HTOP} htop
cd htop
sudo ./autogen.sh
sudo ./configure --prefix=/usr
sudo make --quiet
sudo make --quiet install
cd ..
sudo rm -rf htop
sudo rm -f ${VERSION_HTOP}.tar.gz
echo " "
echo "=============================================================================> Version  htop: "
echo " "
echo "Current version of htop: $(htop --version)"
echo " "
echo "=============================================================================="

echo "=============================================================================="
echo "Step: Install Pandoc - Version ${VERSION_PANDOC}"
echo "------------------------------------------------------------------------------"
wget https://github.com/jgm/pandoc/releases/download/${VERSION_PANDOC}/pandoc-${VERSION_PANDOC}-1-amd64.deb
sudo dpkg -i pandoc-${VERSION_PANDOC}-1-amd64.deb
sudo rm -f pandoc-${VERSION_PANDOC}-1-amd64.deb
echo " "
echo "=============================================================================> Version  Pandoc: "
echo " "
echo "Current version of Pandoc: $(pandoc -v)"
echo " "
echo "=============================================================================="

echo " "
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="

exit 0
