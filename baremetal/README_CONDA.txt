README_CONDA

After setting up a new user with user_setup the user should self-configure with ~/my_setup.sh.

A shared starter environment under /home/we1s-data/envs/env runs on Python 3.7. and has Numpy etc. etc. installed. To activate it, run

    conda activate /home/we1s-data/envs/env

This is the default environment via a line added to the end of .bashrc.

Quick conda commands to create shared or personal conda environments:

Create shared environment:
    conda create -p /home/we1s-data/envs/envname python=3.7
Create personal environment:
    conda create -n envname
Activate shared environment:
    conda activate /home/we1s-data/envs/envname
Activate personal environment:
    conda activate envname
Install packages (in env):
    conda install packagename
Update all packages (in env):
    conda update --all
