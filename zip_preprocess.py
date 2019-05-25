#!/usr/bin/env python3
"""zip_preprocess.py."""

import argparse
import sys
import csv
import json
from shutil import copyfile
import time
import os

from libs.zipeditor.zipeditor import ZipEditor, zip_scanner
from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
from libs.preprocess.preprocess import Preprocessor, content_field_standardize
from libs.deduper.deduper import LinkFilter

def zip_batch_process(zip_dir_root='', source_field='content', preprocessing_log=''):
    """Batch preprocess."""
    # Start the timer
    startBatch = time.time()
    timings = []

    # get list of all zips
    zip_files = zip_scanner(zip_dir_root)
    print(len(zip_files), 'zip files found')

    # create a FuzzyHasher for making and comparing hashes
    fhr = FuzzyHasher(source_field=source_field, prefilter='baggify,lower_alnum')

    # preprocess configuration
    options = {
        'merge_noun_chunks': False,
        'merge_subtokens': False,
        'skip_ents': ['CARDINAL', 'DATE (except months)', 'QUANTITY', 'TIME'],
        'collect_readability_scores': True
        }

    # create a Preprocessor
    pp = Preprocessor()
    
    # create a LinkFilter
    lf = LinkFilter()

    # loop over zips and unpack for editing
    for zip_file in zip_files:
        print("\n---\nOpening:", zip_file)
        startZip = time.time()
        with ZipEditor(zip_file) as zed:
            changed = False
            zed.open()
            manifest_dir = zed.getdir()

            # get file list
            json_files = [entry.path for entry in os.scandir(manifest_dir) if entry.path.endswith(".json")]
            print(len(json_files), 'json files found')

            # loop through json files for fixes and fuzzy hash
            for json_file in json_files:
                with open(json_file, 'r+') as f:
                    data = json.load(f)

                    # fix for non-standard content fields
                    changed_scrub = content_field_standardize(data)

                    # request a hash add, record if it changed the file
                    changed_hash = fhr.add_hash_to_json(data)
                    
                    # modify file only if something changed
                    changed_file = changed_scrub or changed_hash
                    if changed_file:
                        f.seek(0)
                        json.dump(data, f, indent=2)
                        f.truncate()
                        # mark zip for saving if any file changed
                        changed = True

            # deduplicate
            results = fhr.compare_files_in_dir(zed.getdir())
            result_list = [[str(item).replace(zed.getdir()+'/','') for item in row] for row in results]
            if result_list:
                print('\n...duplicates found:', result_list, '\n')
                changed = True
                with open(os.path.join(zed.getdir(),'_duplicates.txt'), "w") as dupefile:
                    writer = csv.writer(dupefile, dialect='excel-tab')
                    for result in result_list:
                        writer.writerow(result)
                
                # create delete list
                lf.links = result_list
                deletes_list = lf.filter_nodes(source='components', filter='remove')
                # print('dl', deletes_list)
                with open(os.path.join(zed.getdir(),'_deletes.txt'), "w") as delfile:
                    for item in deletes_list:
                        delfile.write("%s\n" % item)
            
            else:
                print('\n...no duplicates found.')

            with open(preprocessing_log, 'a') as preprocessing_log:
                try:
                    pp.preprocess_dir(manifest_dir=manifest_dir, content_property='content_scrubbed', kwargs=options)
                    preprocessing_log.write(manifest_dir + ',success\n')
                except:
                    preprocessing_log.write(manifest_dir + ',fail\n')
            changed = True

            if changed:
                print('\n ...saving:', zip_file)
                zed.save()
            print('\n...closing:', zip_file, '\n\n')

        endZip = time.time()
        t = endZip - startZip
        timings.append([t, zip_file])
        print('Processed zip in ' + str(t) + ' seconds.\n\n----------\n\n')

    endBatch = time.time()
    t = endBatch - startBatch
    timings.append([t, "TOTAL"])
    print('\n\n==========\nProcessed all zip files in ' + str(t) + ' seconds.')
    with open(os.path.join(zip_dir_root,'_timings.txt'), "w") as timefile:
        writer = csv.writer(timefile, dialect='excel-tab')
        for timing in timings:
            writer.writerow(timing)
    print(timings)


def test():
    """Test the script.
    
    The base test data is kept in a non-zip extension to 
    avoid accidentally altering its contents. On the test run,
    test the data.
    
    """

    zip_dir_root = os.path.join(os.getcwd(), 'data_zip')
    for filename in ['test.zip.BAK', 'test-reddit.zip.BAK']:
        try:
            source = os.path.join(zip_dir_root, filename)
            dest = os.path.join(zip_dir_root, filename + '.zip')
            copyfile(source, dest)
        except FileNotFoundError:
            print("No such file:", source)
            pass

    # Configure the path to the preprocessing log here
    preprocessing_log = '../preprocessing_log.csv'
    zip_batch_process(zip_dir_root=zip_dir_root, source_field='content', preprocessing_log=preprocessing_log)

def main(args):
    """Collection of actions to execute on run."""
    zip_batch_process(zip_dir_root=args.inpath, source_field=args.content, preprocessing_log=args.log)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     usage='use "%(prog)s --help" for more information',
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('-i', '--inpath', default='.',
                        help='input path for directory of zips, e.g. "../data"')
    PARSER.add_argument('-l', '--log', default='_preprocessing_log.csv',
                        help='output file path for log file, e.g. "_preprocessing_log.csv"')
    PARSER.add_argument('-c', '--content', default='content',
                        help='json file field for source, e.g. "content"')
    # PARSER.add_argument('-d', '--dedupe', action='store_true', help='generate deduplicate analysis, false by default ')
    # PARSER.add_argument('-h', '--hash', action='store_true', help='add fuzzy hashes to articles, false by default ')
    # PARSER.add_argument('-m', '--meta', action='store_true', help='add spacy metadata, false by default')
    if not sys.argv[1:]:
        PARSER.print_help()
        PARSER.exit()
    ARGS = PARSER.parse_args()
    main(ARGS)
