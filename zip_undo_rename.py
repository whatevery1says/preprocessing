#!/usr/bin/env python3

"""zip_undo_rename.py
Given a source path, walk subdirs and
find any zips with a leading _ in the name:

_im-the-old-versino-of-a-zip.zip

...and rename, deleting any file with that name (although the zip_renamer
renamed it):

im-the-old-versino-of-a-zip.zip

"""

import os
from libs.zipeditor.zipeditor import zip_scanner_excludedirs

# source_path = 'data_zip'
source_path = '/home/we1s-data/data/collect'
exclude_list = set(['preprocess-fails'])

zip_files = [(r, file) for r, d, f in os.walk(source_path) for file in f if file.endswith('.zip')]

print(zip_files)
for zip_file in zip_files:
    if(zip_file[1].startswith('_')):
        print('rename:\n  ', os.path.join(zip_file[0],zip_file[1]), '\n  ', os.path.join(zip_file[0],zip_file[1][1:]))
        os.rename(os.path.join(zip_file[0],zip_file[1]), os.path.join(zip_file[0],zip_file[1][1:]))
