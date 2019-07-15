#!/usr/bin/env python3

from datetime import datetime
import json
import os
from zipfile import BadZipFile
from libs.zipeditor.zipeditor import ZipEditor
from libs.zipeditor.zipeditor import zip_scanner_excludedirs

# from libs.zipeditor.zipeditor import zip_scanner_excludedirs

def batch_rename_zip_with_jsons(source_path='.', exclude_list=[''],
                                rename_list={}, inspect=True):
    """Walk from a source path, excluding any excluded directories,
    and rename any zips found (and their json contents) using a dict
    of file name search and replacement strings.
    Renames on first match only.
    """

    zip_files = zip_scanner_excludedirs(source_path=source_path,
                                   exclude_list=exclude_list, join=False)

    print('COUNT:', len(zip_files), 'UNIQ:', len(set(zip_files)))

    for zip_file in zip_files:
        for src in rename_list.keys():
            if zip_file[1].find(src) > -1: # 
                rename_zip_with_jsons(zip_file[0], zip_file[1], src,
                                      rename_list[src], inspect=inspect)
                break  # rename on first match only


def rename_zip_with_jsons(path, zipname, prestr, poststr, inspect=True):
    """Renames zip file and any json files"""

    log='_log_rename.csv'

    if(prestr==poststr):
        return # skip processing
    prestr = prestr.replace('\n', '')
    poststr = poststr.replace('\n', '')

    dt = datetime.today().strftime('%Y%m%d-%H%M')
    
    zip_file = os.path.join(path, zipname)
    zipname_noext = os.path.splitext(zipname)[0]

    with ZipEditor(zip_file) as zed:
        try:
            zed.open()
        except (BadZipFile, PermissionError, RuntimeError) as err:
            print('\n', err.__class__.__name__, ": ", zip_file, err)
            with open(log, 'a') as logfile:
                logfile.write(dt + ',' + 'zip_fail,' + zip_file + ',' + str(err.__class__.__name__) + ': ' + str(err) + '\n')
            return
        try:
            json_files = [os.path.join(r, file) for r, d, f in os.walk(zed.getdir()) for file in f if file.endswith('.json') and not file.startswith('._')]
            found_mismatch = False
            for json_file in json_files:
                tmppath, fname = os.path.split(json_file)
                if zipname_noext not in fname and not found_mismatch:
                    with open(log, 'a') as logfile:
                        logfile.write(dt + ',' + 'json_nomatch,' + fname + ',' + zip_file + '\n')
                    found_mismatch = True
                os.rename(json_file, os.path.join(tmppath, fname.replace(prestr, poststr)))
            if inspect:
                print('\n[INSPECT SAVE]:\n  ', zip_file, '\n  ', os.path.join(path, zipname.replace(prestr, poststr)))
            else:
                print('\n[SAVE]:\n  ', zip_file, '\n  ', os.path.join(path, zipname.replace(prestr, poststr)))
                zed.save(os.path.join(path, zipname.replace(prestr, poststr)))
                os.rename(os.path.join(path, zipname), os.path.join(path, '_' + zipname))
            zed.close()
            with open(log, 'a') as logfile:
                logfile.write(dt + ',' + 'zip_success,' + zip_file + '\n')
        except (json.decoder.JSONDecodeError, KeyError, PermissionError, ValueError) as err:
            # note that the current code never parses the json -- only renames
            # it, so invalid jsons should succeed without errors.
            print('\n', err.__class__.__name__, ": ", json_file, err)
            with open(log, 'a') as logfile:
                logfile.write(dt + ',' + 'json_fail,' + zip_file + '@' + json_file + ',' + str(err.__class__.__name__) + ': ' + str(err) + '\n')
            return


## CONFIGURE VARIABLES

source_path = 'data_zip'
# source_path = '/home/we1s-data/data/collect'

exclude_list = set(['preprocess-fails'])

# rename_list = {
#                '_chicagotribune_': '_thechicagotribune_',
#                '_invalid.' : '_XX-invalid.',
#                '_password.' : '_XX-password.',
#              }
with open('_rename_list.txt') as f:
    rename_list = dict([line.split("\t") for line in f])
print('\nRENAME LIST\n', rename_list, '\n')

batch_rename_zip_with_jsons(source_path=source_path,
                            exclude_list=exclude_list,
                            rename_list=rename_list,
                            inspect=True)
