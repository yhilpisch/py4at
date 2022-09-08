#!/bin/bash
#
# Script to Install
# Linux System Tools and
# Basic Python Components
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
# GENERAL LINUX
apt-get update  # updates the package exit_index cache
apt-get upgrade -y  # updates packages
# installs system tools
apt-get install -y bzip2 gcc git  # system tools
apt-get install -y htop screen vim wget  # system tools
apt-get upgrade -y bash  # upgrades bash if necessary
apt-get clean  # cleans up the package exit_index cache

# INSTALL MINICONDA
# downloads Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O Miniconda.sh
bash Miniconda.sh -b  # installs it
rm -rf Miniconda.sh  # removes the installer
export PATH="/root/miniconda3/bin:$PATH"  # prepends the new path

# INSTALL PYTHON LIBRARIES
conda install -y pandas  # installs pandas
conda install -y ipython  # installs IPython shell
conda install -y scipy #from scipy.optimize import brute
conda install -y pylap #Plotting grafic
conda install -c conda-forge ta

#Git solution but you need to install git
#mkdir "trading"
#cd trading/
#git clone https://github.com/GianniGithub/GiannisTraidingReserching.git
#git checkout Mac_arm64

# CUSTOMIZATION
#cd /root/
#wget http://hilpisch.com/.vimrc  # Vim configuration
