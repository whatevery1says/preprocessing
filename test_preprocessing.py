"""test_preprocessing.py.

Tests odd or even numbered json files in zip archives in a 
directory to see if they contain required properties. The 
script does not test whether the preprocessor has sent 
outputs to the wikifier.
"""

# Python imports
import argparse
import json
import os
import sys
from json import JSONDecodeError
from zipfile import ZipFile, BadZipFile

# Functions
def get_file_list(zip_file, check='odd'):
    """Return a list of odd or even numbered files in the zip archive."""
    print('Getting ' + check + ' files in ' + zip_file + '...')
    zip = ZipFile(zip_file)
    json_files = zip.namelist()
    if check == 'even':
        json_files = [file for i, file in enumerate(json_files) if i % 2 == 0]
    else:
        json_files = [file for i, file in enumerate(json_files) if i % 2 is not 0]
    return json_files

def read_file(zip_dir, zip_file, file, log_file):
    """Read a json file and return a Python dict."""
    zip = ZipFile(os.path.join(zip_dir, zip_file))
    try:
        with zip.open(file) as f:
            return json.loads(f.read())
    except (BadZipFile, JSONDecodeError, UnicodeDecodeError, PermissionError, RuntimeError) as err:
        log_errors(log_file, zip_dir, zip_file, file, err)
        return {}

def test(doc):
    """Test a json file for required properties.

    Returns a list of missing properties.

    """
    errors = []
    manifest_properties = ['name', 'namespace', 'metapath', 'title']
    preprocessing_properties = ['features', 'bag_of_words', 'word_count', 'readability_scores', 'language_model']
    # Test for missing manifest properties
    for prop in manifest_properties:
        try:
            assert prop in doc
        except AssertionError:
            errors.append(prop)
    # Test for missing preprocessing properties
    for prop in preprocessing_properties:
        try:
            assert prop in doc
        except AssertionError:
            errors.append(prop)
    return errors

def log_errors(log_file, zip_dir, zip, file, result):
    """Write errors to the test log file."""
    with open(log_file, 'a') as f:
        f.write(zip_dir + '/' + zip + ',' + file + ',' + str(result) + '\n')

def main(args):
    """Execute on run."""
    zip_dir = args.zip_dir
    log_file = args.log_file
    check = args.check

    # Iterate through the zip archives in the directory
    zip_files = [file for file in os.listdir(zip_dir) if file.endswith('.zip')]
    for zip_file in zip_files:
        # Get a list of even or odd files in the zip archive
        try:
            # testzip = ZipFile(os.path.join(zip_dir, zip_file))
            json_file_list = get_file_list(os.path.join(zip_dir, zip_file), check)
            # Iterate through the json files in the list
            for file in json_file_list:
                # Read the json and perform test
                doc = read_file(zip_dir, zip_file, file, log_file)
                result = test(doc)
                # Log any errors
                if len(result) > 0:
                    log_errors(log_file, zip_dir, zip_file, file, result)
        except BadZipFile as err:
            log_errors(log_file, zip_dir, zip_file, '', err)
            pass


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__,
                                     usage='use "%(prog)s --help" for more information',
                                     formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('-z', '--zip_dir', default='.',
                        help='input path for directory of zips, e.g. "../data"')
    PARSER.add_argument('-l', '--log_file', default='_log.csv',
                        help='output file path for log file, e.g. "_test_preprocessing_log.csv"')
    PARSER.add_argument('-c', '--check', default='odd',
                        help='setting for whether to check "even" or "odd" json files in each zip archive"')
    if not sys.argv[1:]:
        PARSER.print_help()
        PARSER.exit()
    ARGS = PARSER.parse_args()
    main(ARGS)