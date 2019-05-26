#!/usr/bin/env python3
"""zip_preprocess.py."""

import argparse
import sys
import csv
import json
import time
import os

from libs.zipeditor.zipeditor import ZipEditor, zip_scanner
from zipfile import BadZipFile
from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
from libs.preprocess.preprocess import Preprocessor, content_field_standardize
from libs.deduper.deduper import LinkFilter

def zip_batch_process(zip_dir_root='', source_field='content', preprocessing_log='_preprocessing_log.csv', wikifier_output_dir='wikifier', skip_rerun=False):
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

    skip_files = []
    if(skip_rerun and preprocessing_log):
        try:
            with open(preprocessing_log, 'r') as plogfile:
                reader = csv.reader(plogfile)
                for row in reader:
                    skip_files.append(row[1])
        except FileNotFoundError as err:
            print("Preprocessing log file not found, will create while logging.")

    # create a Preprocessor
    pp = Preprocessor()
    
    # create a LinkFilter
    lf = LinkFilter()

    # loop over zips and unpack for editing
    for zip_file in zip_files:
        # skip
        if(skip_rerun and zip_file in skip_files):
            print("\n---\nSkipping:", zip_file)
            continue
        print("\n---\nOpening:", zip_file)
        startZip = time.time()
        with ZipEditor(zip_file) as zed:
            changed = False
            try:
                zed.open()
            except BadZipFile as err:
                print(err.__class__.__name__, ": ", zip_file, err)
                continue
            
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
                print('\n...duplicates found:', str(len(result_list)), '\n')
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

            # create the wikifier output directory. setting the preprocessor wikifier_output_dir property activates outputting during the preprocess
            pp.wikifier_output_dir = os.path.join(wikifier_output_dir, os.path.basename(zed.file).rsplit('.zip')[0])
            os.makedirs(pp.wikifier_output_dir, exist_ok=True)
            
            with open(preprocessing_log, 'a') as plogfile:
                try:
                    pp.preprocess_dir(manifest_dir=manifest_dir, content_property='content', kwargs=options)
                    plogfile.write('done,' + zip_file + '\n')
                    changed = True
                except KeyError as err:
                    print(err)
                    plogfile.write('fail,' + manifest_dir + ',' + str(err) + '\n')

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


def main(args):
    """Collection of actions to execute on run."""
    zip_batch_process(zip_dir_root=args.inpath, source_field=args.content, preprocessing_log=args.log, wikifier_output_dir=args.wiki, skip_rerun=args.skip)


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
    PARSER.add_argument('-w', '--wiki', default='wikifier',
                        help='output directory path for wikifier data, e.g. "wikifier"')
    PARSER.add_argument('-s', '--skip', action='store_true',
                        help='skip rerun of any files already listed in log, whether done or fail; false by default')
    # PARSER.add_argument('-d', '--dedupe', action='store_true', help='generate deduplicate analysis, false by default ')
    # PARSER.add_argument('-h', '--hash', action='store_true', help='add fuzzy hashes to articles, false by default ')
    # PARSER.add_argument('-m', '--meta', action='store_true', help='add spacy metadata, false by default')
    if not sys.argv[1:]:
        PARSER.print_help()
        PARSER.exit()
    ARGS = PARSER.parse_args()
    main(ARGS)
