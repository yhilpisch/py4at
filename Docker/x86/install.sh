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
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh
bash Miniconda.sh -b  # installs it
rm -rf Miniconda.sh  # removes the installer
export PATH="/root/miniconda3/bin:$PATH"  # prepends the new path
export PYTHONPATH="${PYTHONPATH}:/runfolder/"  # https://towardsdatascience.com/how-to-fix-modulenotfounderror-and-importerror-248ce5b69b1c

# INSTALL PYTHON LIBRARIES
conda install -y pandas  # installs pandas
conda install -y ipython  # installs IPython shell
conda install -y scipy #from scipy.optimize import brute
conda install -y pylap #Plotting grafic
conda install -c conda-forge ta
conda install -c conda-forge matplotlib #Plotter
conda install -c conda-forge telegram-send


# CUSTOMIZATION
cd ~/ || exit
wget http://hilpisch.com/.vimrc  # Vim configuration

# telegrambot
cp /runfolder/config/telegram-send.conf /etc/
telegram-send -g "image build"

cd /runfolder || exit
#OUTPUT=$(python Run_backtest.py); telegram-send -g "${OUTPUT}"
