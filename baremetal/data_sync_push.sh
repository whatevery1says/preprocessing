#!/usr/bin/env bash

declare -a datadirs=("parsed"
                     )

for i in "${datadirs[@]}"
do
   echo "$i"
   rsync -e 'ssh -p 9001 -l root' -chavzP --stats --chown=1000:users \
     "/home/we1s-data/data/${i}/" \
     "harbor.english.ucsb.edu:/data/${i}"
   # sudo chown -R 1000:users "/home/we1s-data/data/${i}/"
   # sudo chmod -R 775 "/home/we1s-data/data/${i}/"
done
