#!/usr/bin/env python3

from datetime import datetime
import json
import os
from zipfile import BadZipFile

import sys
sys.path.append(".")

from libs.zipeditor.zipeditor import ZipEditor
from libs.zipeditor.zipeditor import zip_scanner_excludedirs
from libs.preprocess.preprocess import source_field_from_filename

# from libs.zipeditor.zipeditor import zip_scanner_excludedirs

def batch_mod_zip_with_jsons(source_path='.', inspect=True):

    zip_files = zip_scanner_excludedirs(source_path=source_path,
                                   exclude_list=[], join=False)

    print('COUNT:', len(zip_files), 'UNIQ:', len(set(zip_files)))

    for zip_file in zip_files:
        recontent_jsons(zip_file[0], zip_file[1], inspect=inspect)

def recontent_jsons(path, zipname, inspect=True):
    """Renames zip file and any json files"""

    zip_file = os.path.join(path, zipname)
    zipname_noext = os.path.splitext(zipname)[0]

    with ZipEditor(zip_file) as zed:
        try:
            zed.open()
        except (BadZipFile, PermissionError, RuntimeError) as err:
            print('\n', err.__class__.__name__, ": ", zip_file, err)
        try:
            print('\n\nZIP: ', zip_file, '\n-----------\n')
            json_files = [os.path.join(r, file) for r, d, f in os.walk(zed.getdir()) for file in f if file.endswith(('.json')) and not file.startswith('._')]
            # found_mismatch = False
            for json_file in json_files:

                namestr = os.path.splitext(os.path.basename(json_file))[0]
                ## AND JSON FOR PASSING

                with open(json_file, 'r+') as f:
                    try:
                        data = json.load(f)
                        source_field_from_filename(namestr, data)
                        print("sources: ", data['sources'])
                        print("metapath:", data['metapath'])
                        print("name:    ", data['name'], '\n')
                    except (json.decoder.JSONDecodeError, KeyError, PermissionError, ValueError) as err:
                        print('\n', err.__class__.__name__, ": ", json_file,  err)

            # if inspect:
            #     print('\n[INSPECT SAVE]:\n  ', zip_file, '\n  ', os.path.join(path, zipname.replace(prestr, poststr)))
            #     source_field_from_filename(namestr, data)
            # else:
            #     print('\n[SAVE]:\n  ', zip_file, '\n  ', os.path.join(path, zipname.replace(prestr, poststr)))
            #     zed.save(os.path.join(path, zipname.replace(prestr, poststr)))
            #     os.rename(os.path.join(path, zipname), os.path.join(path, '_' + zipname))
            zed.close()

        except (json.decoder.JSONDecodeError, KeyError, PermissionError, ValueError) as err:
            # note that the current code never parses the json -- only renames
            # it, so invalid jsons should succeed without errors.
            print('\n', err.__class__.__name__, ": ", err)



# source_path = 'data_zip'
source_path = 'data_zip'
batch_mod_zip_with_jsons(source_path=source_path, inspect=True)
