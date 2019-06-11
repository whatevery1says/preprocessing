#!/usr/bin/env bash

declare -a datadirs=("collect"
                     )

for i in "${datadirs[@]}"
do
   echo "$i"
   rsync -e 'ssh -p 9001 -l root' -chavzP --stats --chown=jovyan:users \
     "harbor.english.ucsb.edu:/data/${i}/" \
     "/home/we1s-data/data/${i}/"
   # sudo chown -R 1000:users "/home/we1s-data/data/${i}/"
   # sudo chmod -R 775 "/home/we1s-data/data/${i}/"
done
