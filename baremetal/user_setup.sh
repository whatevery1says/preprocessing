#!/usr/bin/env bash

# Create a new user

USERNAME=$1
adduser ${USERNAME}
usermod -a -G users ${USERNAME}
usermod -a -G we1s-data ${USERNAME}
cp my_setup.sh /home/${USERNAME}/
