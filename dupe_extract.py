#!/usr/bin/env python3
"""dupe_extract.py."""

import argparse
import io
import sys
import csv
import os
import zipfile

from libs.zipeditor.zipeditor import zip_scanner


def dupe_extract(zip_dir_root='', output_dir='dupe_inspect'):
    """Takes a directory of zips that has already been.
    analyzed for duplicates. Copies out the duplicate pair
    listings and example JSON files into an output directory
    for inspection.
    """
    # get list of all zips
    zip_files = zip_scanner(zip_dir_root)
    print(len(zip_files), 'zip files found')
    
    dupes_all = []
    deletes_all = []

    os.makedirs(output_dir, exist_ok=True)

    # loop over zips and unpack for editing
    for zip_file in zip_files:
        print("\n---\nOpening:", zip_file)

        with zipfile.ZipFile(zip_file, 'r') as zfile:
            # create per-zip output subdirectory for duplicate json examples
            zip_output_dir = os.path.join(output_dir, os.path.basename(zip_file).rsplit('.zip')[0])
            os.makedirs(zip_output_dir, exist_ok=True)

            # duplicates
            zfile_dupes = io.TextIOWrapper(zfile.open('_duplicates.txt', 'r')).readlines()
            print(' ...copying ', len(zfile_dupes), 'duplicate pairs')
            dupes_all.extend(zfile_dupes)
            zfile.extract('_duplicates.txt', path=zip_output_dir, pwd=None)

            # examples -- copy duplicate json examples to subdirectory
            print(' ...copying duplicates to subfolder: ', zip_output_dir)
            for zdupe_row in zfile_dupes:
                zdupe_row = zdupe_row.split('\t')
                zfile.extract(zdupe_row[1].strip(), path=zip_output_dir, pwd=None)
                zfile.extract(zdupe_row[2].strip(), path=zip_output_dir, pwd=None)
        
            # deletes
            zfile_deletes = io.TextIOWrapper(zfile.open('_deletes.txt', 'r')).readlines()
            print(' ...copying delete recommendations')
            for zd in zfile_deletes:
                deletes_all.append(zd)
            zfile.extract('_deletes.txt', path=zip_output_dir, pwd=None)

    # save combined duplicate pairs
    with open(os.path.join(output_dir,'_duplicates_all.txt'), "w") as dupefile:
        for dupe in dupes_all:
            dupefile.write(dupe)

    # save combined delete recommendations
    with open(os.path.join(output_dir,'_deletes_all.txt'), "w") as delfile:
        for delete in deletes_all:
            delfile.write(delete)


def main(args):
    """Collection of actions to execute on run."""
    dupe_extract(zip_dir_root=args.inpath, output_dir=args.outpath)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     usage='use "%(prog)s --help" for more information',
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('-i', '--inpath', default='.',
                        help='input path for directory of zips')
    PARSER.add_argument('-o', '--outpath', default='dupe_inspect',
                        help='output path for inspection files')
    if not sys.argv[1:]:
        dupe_extract(zip_dir_root='data_zip')
        # PARSER.print_help()
        PARSER.exit()
    ARGS = PARSER.parse_args()
    main(ARGS)
