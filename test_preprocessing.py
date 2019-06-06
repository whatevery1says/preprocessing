"""test_preprocessing.py.

Tests odd or even numbered json files in zip archives in a 
directory to see if they contain required properties. The 
script does not test whether the preprocessor has sent 
outputs to the wikifier.

Development Notes:

- The log file should probably append the zip_dir to the 
zipfile name.
- Configuration should probably be changed to run through the
command line.
"""

# Python imports
import json
import os
from json import JSONDecodeError
from zipfile import ZipFile, BadZipFile

# Configuration
zip_dir = 'data_zip'
log_file = 'data_zip_bk/test_log.csv'

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

def read_file(zip_file, file):
    """Read a json file and return a Python dict."""
    zip = ZipFile(os.path.join(zip_dir, zip_file))
    try:
        with zip.open(file) as f:
            return json.loads(f.read())
    except JSONDecodeError:
        log_errors(log_file, zip_file, file, 'JSONDecodeError')
        return {}
    except UnicodeDecodeError:
        log_errors(log_file, zip_file, file, 'UnicodeDecodeError')
        return {}
    except RuntimeError:
        log_errors(log_file, zip_file, file, 'RuntimeError')
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

def log_errors(log_file, zip, file, result):
    """Write errors to the test log file."""
    with open(log_file, 'a') as f:
        f.write(zip + ',' + file + ',' + str(result) + '\n')


# Iterate through the zip archives in the directory
for zip_file in os.listdir(zip_dir):
    # Get a list of even or odd files in the zip archive
    try:
        # testzip = ZipFile(os.path.join(zip_dir, zip_file))
        json_file_list = get_file_list(os.path.join(zip_dir, zip_file), 'odd')
        # Iterate through the json files in the list
        for file in json_file_list:
            # Read the json and perform test
            doc = read_file(zip_file, file)
            result = test(doc)
            # Log any errors
            if len(result) > 0:
                log_errors(log_file, zip_file, file, result)
    except BadZipFile:
        log_errors(log_file, zip_file, '', 'BadZipFile')
        pass
