"""test_preprocessing.py.

Tests odd or even numbered json files in zip archives in a 
directory to see if they contain required properties.

Note: Some functions may require configuration of file paths
with `os.path.join()`. Also, the script does not test whether
the preprocessor has sent outputs to the wikifier.

Also configuration should probably be changed to run through the
command line.
"""

# Python imports
import json
import os
from zipfile import ZipFile

# Configuration
zip_dir = ''
log_file = ''

# Functions
def get_file_list(zip_file, check='odd'):
    """Return a list of odd or even numbered files in the zip archive."""
    zip = ZipFile(zip_file)
    json_files = zip.namelist()
    if check == 'even':
        json_files = [file for i, file in enumerate(json_files) if i % 2 == 0]
    else:
        json_files = [file for i, file in enumerate(json_files) if i % 2 is not 0]
    return json_files

def read_file(zip, file):
    """Read a json file and return a Python dict."""
    with zip.open(file) as f:
        return json.loads(f.read())

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
        except ValueError:
            errors.append(prop)
    # Test for missing preprocessing properties
    for prop in preprocessing_properties:
        try:
            assert prop in doc
        except ValueError:
            errors.append(prop)
    return errors

def log_errors(log_file, zip, file, result):
    """Write errors to the test log file."""
    with open(log_file, 'a') as f:
        f.write(zip + ',' + file + ',' + str(result))


# Iterate through the zip archives in the directory
for zip in zip_dir:
    # Get a list of even or odd files in the zip archive
    json_file_list = get_file_list(zip, 'odd')
    # Iterate through the json files in the list
    for file in json_file_list:
        # Read the json and perform test
        doc = read_file(zip, file)
        result = test(doc)
        # Log any errors
        if len(result) > 0:
            log_errors(log_file, zip, file, result)

