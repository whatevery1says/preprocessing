"""zip_preprocess.py."""

import csv
import json
from shutil import copyfile
import time
import os

from libs.zipeditor.zipeditor import ZipEditor, zip_scanner
from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
from libs.preprocess.preprocess import Preprocessor, content_field_standardize

def zip_batch_process(zip_dir_root='', source_field='content'):
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
            result_list = [result for result in results]
            if result_list:
                print('\n...duplicates found:', result_list, '\n')
                changed = True
                with open(os.path.join(zed.getdir(),'_duplicates.txt'), "w") as dupefile:
                    writer = csv.writer(dupefile, dialect='excel-tab')
                    for result in result_list:
                        writer.writerow(result)
            else:
                print('\n...no duplicates found.')

            ##################
            # RUN PREPROCESSOR
            ##################
            # I have refactored preprocess_dir into a class in
            # libs/preprocess/preprocess.py Preprocessor.preprocess_dir.
            #
            # However, things were *really* complicated, with tons of
            # global variables and state, including complex shared global
            # dependencies with the Document class, so I'm not confident
            # that this was done correctly -- it needs Scott to do a code
            # review.
            pp.preprocess_dir(manifest_dir=manifest_dir, content_property=source_field, kwargs=options)
            # right now pre-processing can't indicate no change -- if it COULD
            # then we could skip re-compressing and copying zips that
            # don't need to be  updated. This would greatly increase performance
            # time on subsequent runs to correct individual fields or add
            # supplemental metadata to small batches of new files.
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
    the test data.
    
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
    zip_batch_process(zip_dir_root=zip_dir_root, source_field='content')
    

if __name__ == '__main__':
    test()
