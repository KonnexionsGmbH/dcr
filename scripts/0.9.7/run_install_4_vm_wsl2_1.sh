#!/bin/bash

set -e

# ----------------------------------------------------------------------------------
#
# run_install_4_vm_wsl2_1.sh: Install a dcr_dev environment for Ubuntu 20.04 - Step 1.
#
# ----------------------------------------------------------------------------------

sudo rm -rf /tmp/*

export HOST_ENVIRONMENT_DEFAULT=vm

export VERSION_DCR_DEV=0.9.7

export VERSION_DBEAVER=22.2.0
export VERSION_HTOP=3.2.1
export VERSION_OPENSSL=1_1_1o
export VERSION_PANDOC=2.19.2
export VERSION_POPPLER=22.02.0
export VERSION_PYTHON3=3.10.7
export VERSION_TMUX=3.3a

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
                         build-essential \
                         byacc \
                         ca-certificates \
                         cmake \
                         curl \
                         dos2unix \
                         e2fslibs-dev \
                         gcc \
                         git \
                         gnupg \
                         libaudit-dev \
                         libblkid-dev \
                         libboost-all-dev \
                         libbz2-dev \
                         libcairo2-dev  \
                         libffi-dev \
                         libgif-dev \
                         libjpeg-dev \
                         libjpeg-turbo8 \
                         liblzma-dev \
                         libncurses-dev \
                         libncurses5-dev \
                         libncursesw5-dev \
                         libnss3  \
                         libnss3-dev \
                         libopenjp2-7 \
                         libopenjp2-7-dev \
                         libpng-dev \
                         libreadline-dev \
                         libsqlite3-dev \
                         libssl-dev \
                         libtiff-dev \
                         libwebp-dev \
                         libxml2-dev \
                         libxmlsec1-dev \
                         libz-dev \
                         llvm \
                         locales \
                         lsb-release \
                         make \
                         pkg-config \
                         poppler-utils \
                         procps \
                         software-properties-common \
                         texlive-base \
                         texlive-xetex \
                         tk-dev \
                         tzdata \
                         unzip \
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
eval echo 'export VERSION_OPENSSL=${VERSION_OPENSSL}' >> ${HOME}/.bashrc
eval echo 'export VERSION_PANDOC=${VERSION_PANDOC}' >> ${HOME}/.bashrc
eval echo 'export VERSION_POPPLER=${VERSION_POPPLER}' >> ${HOME}/.bashrc
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
# from Docker Desktop --------------------------------------------------------------
if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    echo '' >> ${HOME}/.bashrc
    echo 'if [ `id -gn` != "docker" ]; then ( newgrp docker ) fi' >> ${HOME}/.bashrc
fi

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

if [ "${HOST_ENVIRONMENT}" = "vm" ]; then
    echo "------------------------------------------------------------------------------"
    echo "Step: Install Docker Desktop"
    echo "------------------------------------------------------------------------------"
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" --yes
    sudo apt-key fingerprint 0EBFCD88
    sudo apt-get install -qy docker-ce \
                             docker-ce-cli \
                             containerd.io
    sudo chmod 666 /var/run/docker.sock
    if ! [ $(getent group docker | grep -q "\b$USER\b") ]; then
        sudo usermod -aG docker $USER
    fi
    docker ps     | grep "portainer"           && docker stop portainer
    docker ps -a  | grep "portainer"           && docker rm --force portainer
    docker images | grep "portainer/portainer" && docker rmi -f portainer/portainer
    docker run -d --name portainer -p 8000:8000 -p 9000:9000 -v "//var/run/docker.sock/":/var/run/docker.sock -v "/Home/portainer/":/data portainer/portainer
    echo " "
    echo "=============================================================================> Version  Docker Desktop: "
    echo " "
    echo "Current version of Docker Desktop: $(docker version)"
    echo " "
    echo "=============================================================================="
fi

echo "------------------------------------------------------------------------------"
echo "Step: Install htop - Version ${VERSION_HTOP}"
echo "------------------------------------------------------------------------------"
wget --quiet --no-check-certificate -nv https://github.com/htop-dev/htop/archive/${VERSION_HTOP}.tar.gz
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
echo "Step: Install OpenSSL - Version ${VERSION_OPENSSL}"
echo "------------------------------------------------------------------------------"
wget --quiet --no-check-certificate -nv https://github.com/openssl/openssl/archive/OpenSSL_${VERSION_OPENSSL}.tar.gz
sudo tar -xf OpenSSL_${VERSION_OPENSSL}.tar.gz
sudo rm -rf openssl
sudo mv openssl-OpenSSL_${VERSION_OPENSSL} openssl
pwd
ls -ll
cd openssl
sudo ./config
sudo make --quiet
sudo make --quiet install
cd ..
sudo ldconfig
sudo rm -rf openssl
sudo rm -f OpenSSL_*.tar.gz
echo " "
echo "=============================================================================> Version  OpenSSL: "
echo " "
echo "Current version of OpenSSL: $(openssl version -a)"
echo " "
echo "=============================================================================="

echo "=============================================================================="
echo "Step: Install Pandoc - Version ${VERSION_PANDOC}"
echo "------------------------------------------------------------------------------"
wget --quiet https://github.com/jgm/pandoc/releases/download/${VERSION_PANDOC}/pandoc-${VERSION_PANDOC}-1-amd64.deb
sudo dpkg -i pandoc-${VERSION_PANDOC}-1-amd64.deb
sudo rm -f pandoc-${VERSION_PANDOC}-1-amd64.deb
echo " "
echo "=============================================================================> Version  Pandoc: "
echo " "
echo "Current version of Pandoc: $(pandoc -v)"
echo " "
echo "=============================================================================="

echo "=============================================================================="
echo "Step: Install Poppler - Version ${VERSION_POPPLER}"
echo "------------------------------------------------------------------------------"
wget --quiet https://poppler.freedesktop.org/poppler-${VERSION_POPPLER}.tar.xz
sudo tar -xf poppler-${VERSION_POPPLER}.tar.xz
cd poppler-${VERSION_POPPLER}/
sudo mkdir build
cd build
sudo cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DTESTDATADIR=$PWD/testfiles -DENABLE_UNSTABLE_API_ABI_HEADERS=ON ..
sudo make
sudo make install
cd ../..
sudo rm -f poppler-${VERSION_POPPLER}.tar.xz
echo " "
echo "=============================================================================> Version  Poppler: "
echo " "
echo "Current version of Poppler: $(pdftocairo -v)"
echo " "
echo "=============================================================================="

echo "------------------------------------------------------------------------------"
echo "Step: Install Tesseract OCR"
echo "------------------------------------------------------------------------------"
sudo add-apt-repository -y ppa:alex-p/tesseract-ocr-devel
sudo apt-get update -qy
sudo apt-get install -qy tesseract-ocr
sudo apt-get install -qy tesseract-ocr-deu
sudo apt-get install -qy tesseract-ocr-eng
sudo apt-get install -qy tesseract-ocr-fra
sudo apt-get install -qy tesseract-ocr-ita
echo " "
echo "=============================================================================> Version Tesseract OCR: "
echo " "
echo "Current version of Tesseract OCR: $(tesseract --version)"
echo " "
tesseract --list-langs
echo " "
echo "=============================================================================="

echo " "
echo "------------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "------------------------------------------------------------------------------"
echo "End   $0"
echo "=============================================================================="

exit 0
