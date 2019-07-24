import json
import os

class BatchJSONUploader:
    """Processor takes a file path, iterates over JSON files,
    and uploads to a mongodb database.
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

    def do(self, files_path):
        # create delete list
        with open(os.path.join(files_path, self.deletes_file), 'r') as f:
            self.deletes_list = f.read().splitlines()
        self.json_paths = [os.path.join(r, file) for r, d, f in os.walk(files_path) for file in f if file.endswith('.json') and not file.startswith('._')]
        for json_path in self.json_paths:
            try:
                json_basename = os.path.split(json_path)[1]
                json_data=None
                with open(json_path, 'r+') as f:
                    json_data = json.load(f)
                if json_path in self.deletes_list:
                    self.deletes_collection.insert_one(json_data)
                elif self.filter_name_must and self.filter_name_must not in json_basename:
                    self.filter_collection.insert_one(json_data)
                elif self.filter_name_cant and self.filter_name_must in json_basename:
                    self.filter_collection.insert_one(json_data)
                else:
                    self.default_collection.insert_one(json_data)
            except (json.decoder.JSONDecodeError, KeyError, PermissionError, ValueError) as err:
                print('\n', err.__class__.__name__, ": ", json_path, err)
                continue
