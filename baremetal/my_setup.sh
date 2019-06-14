#!/usr/bin/env bash

cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
echo 'conda activate /home/we1s-data/envs/env' >>~/.bash_profile
./Miniconda3-latest-Linux-x86_64.sh
echo 'Now log out then in to find conda. Default env will load from .bashrc'
