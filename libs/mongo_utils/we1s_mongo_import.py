"""we1s_mongo_import.py
Combine imported ZipProcessor and a custom BatchJSONUploader2
(prev version was added to ziputils)
"""

import json
import os
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError, InvalidDocument
import sys

sys.path.insert(0, '/home/jovyan/utils/preprocessing/')
from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
from libs.zipeditor.zipeditor import ZipEditor, zip_scanner, zip_scanner_excludedirs, ZipProcessor
from we1s_utils.ziputils import BatchJSONUploader

class BatchJSONUploader2:
    """Processor takes a file path, iterates over JSON files,
    and uploads to a mongodb database.
    If a criteria matches, such as being listed in deletes
    or a name matching cant or must, then a document is either
    inserted (if a target collection is provided) or skipped.
    If no rules match, then documents will be uploaded to the
    default collection (if provided).
    """

    def __init__(self,
        default_collection,             # 'humanities-keywords'
        deletes_collection='deletes',   # 'deletes-humanities'
        deletes_file = '_deletes.txt',  # '_deletes.txt'
        filter_collection='filter',     #
        filter_name_cant='',            # 'no-exact-match'
        filter_name_must=''
        ):         # 'humanities-keywords-no-exact-match'

        self.default_collection = default_collection
        self.deletes_collection = deletes_collection
        self.deletes_file = deletes_file
        self.filter_collection = filter_collection
        self.filter_name_cant = filter_name_cant
        self.filter_name_must = filter_name_must

    def get_json(json_path):
        json_data = None
        with open(json_path, 'r+') as f:
            json_data = json.load(f)
            json_data.pop('bag_of_words', None)
        return json_data
        
    def do(self, files_path):
        # create delete list
        try:
            with open(os.path.join(files_path, self.deletes_file), 'r') as f:
                self.deletes_list = f.read().splitlines()
        except OSError:
            self.deletes_list = []
        self.json_paths = [os.path.join(r, file) for r, d, f in os.walk(files_path) for file in f if file.endswith('.json') and not file.startswith('._')]
        for json_path in self.json_paths:
            try:
                json_basename = os.path.split(json_path)[1]
                if json_basename in self.deletes_list:
                    if self.deletes_collection:
                        self.deletes_collection.insert_one(get_json(json_path))
                elif self.filter_name_must and self.filter_name_must not in json_basename:
                    if self.filter_collection:
                        self.filter_collection.insert_one(get_json(json_path))
                elif self.filter_name_cant and self.filter_name_cant in json_basename:
                    if self.filter_collection:
                        self.filter_collection.insert_one(get_json(json_path))
                elif self.default_collection:
                    self.default_collection.insert_one(get_json(json_path))
            except (json.decoder.JSONDecodeError, KeyError, PermissionError, ValueError, InvalidDocument) as err:
                print('\n', err.__class__.__name__, ": ", json_path, err)
                continue
