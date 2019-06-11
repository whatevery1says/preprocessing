README_BAREMETAL


OOPS -- checked in scripts to git need permissions set correctly



The live sync scripts are currently in /home/jovyan/ and (should be) backed up to the repo in preprocessing/baremetal/

To pull:

su - jovyan
cd ~
# pull data from collector -- from harbor:data/collect
data_sync_pull.sh

To prep:

Copy zip files from collect into the appropriate parsed subfolders.
This is where merging and updating happens.
When replacing and old zip with a new zip of the same name, note that it will get skipped if listed in the log file -- remov

To push:

su - jovyan
cd ~
# push data for notebooks to harbor:data/parsed
data_sync_push.sh




/home/we1s-data/preprocessing


Research accounts are members of

users
we1s-data



Write down basic instructions for using baremetal -- baremetal 

README in tools repo

-  on Ryver
-  push
-  pull
-  copy things over and run a job as jovyan
   -  conda environment

-  zip_preprocess wikifier by default pollutes the sync directory -- move that data out

-  Dan access to wikifier data -- copy into user directory? in script?





Our fully processed data is now fully synced!
The scripts on baremetal are:

/home/jovyan/data_sync_pull.sh
/home/jovyan/data_sync_push.sh
The data copied from collector to baremetal:

pulled
from: collector:/data/collect/
to: baremetal:/home/we1s-data/collect/
total size is 13.24G

That same data pushed from baremetal to notebooks, after being preprocessed and parsed / enriched with metadata:

pushed
from: baremetal:/home/we1s-data/parsed/
to: notebooks:/data/parsed/
total size is 25.92G





$ # move data to junqing home
$ sudo mv /home/we1s-data/data/wikifier/ /home/junqing/wikifier/

$ # set permissions
$ sudo chown -R junqing:users /home/junqing/wikifier
$ sudo chmod -R 755 /home/junqing/wikifier/

$ # add dan and junqing to shared users group
$ sudo usermod -a -G users baciu
$ sudo usermod -a -G we1s-data baciu
$ sudo usermod -a -G users junqing
$ sudo usermod -a -G we1s-data junqing







