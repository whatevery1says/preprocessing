#!/usr/bin/env python3
"""Save items in a _wishlist.txt or configure to load
from this script. script scans the source_path and
logs all _wishlist.txt zip entries not found on the path
to _log_wishlist.csv"""

from datetime import datetime
from libs.zipeditor.zipeditor import zip_scanner_excludedirs


source_path='data_zip'

exclude_list = set(['preprocess-fails'])


load_wishlist = True
if(load_wishlist):
    with open('_wishlist.txt', 'r') as f:
        wishlist = set([line.strip() for line in f])
else:
    wishlist = set([
       '8119_8119_thechicagotribune_subfolder.zip',
       'json_XX-invalid.zip',
       'nothere.zip',
       'zip_good.zip',
       ])
print('\nWISHLIST\n', wishlist, '\n')

zip_files = zip_scanner_excludedirs(source_path=source_path,
                                    exclude_list=exclude_list, join=False)
zip_names_dict = list(list(zip(*zip_files))[1])
zip_names_dict.sort()

with open('_log_wishlist.csv', 'a') as logfile:
    dt = datetime.today().strftime('%Y%m%d-%H%M')
    msg = '\n--- ' + dt + ' ---'
    print(msg)
    logfile.write(msg + '\n')
    for wish in wishlist:
        if wish not in zip_names_dict:
            print('missing,', wish)
            logfile.write('missing, '+ wish + '\n')
