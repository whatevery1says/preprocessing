import json
import os
import unittest
from pymongo import MongoClient 

import sys
sys.path.append(".")

from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
from libs.zipeditor.zipeditor import ZipEditor, zip_scanner, ZipProcessor
from we1s_utils.ziputils import BatchJSONUploader

class TestFuzzyZipEditor(unittest.TestCase):
    """Tests for the ZipEditor + FuzzyHasher."""
   
    azipfile = '6742_thenewyorktimes_bodyartpre1singularhistoryorhleadartpre1singularhistory_2012-01-01_2012-12-31.zip'

    zipfiles = zip_scanner('data')
    print(zipfiles)

    def test_with_open_save_close(self):
        """Test with context for open, save, close of a ZIP file.
        """
        with ZipEditor(self.azipfile) as zed:
            zed.open()
            files = [entry.path for entry in os.scandir(zed.tmpdir.name) if entry.path.endswith(".json")]
            h = FuzzyHasher(source_field='content',
                            hash_field='content-hash-ssdeep')
            
            # all hash
            for file in files:
                change = h.add_hash_to_json_file(file)
                if change:
                    print(change)
                else:
                    print('skip')
            
            zed.save(outfile=None)
            # print(files)

    def test_mongo_upload(self):
        client = MongoClient('mongodb://mongo/')
        db = client['we1s']
        hum_uploader = BatchJSONUploader(
            default_collection=db['humanities-keywords'],
            deletes_file = '_deletes.txt',
            deletes_collection=db['deletes-humanities'],
            filter_name_cant='no-exact-match',
            filter_name_must='',
            filter_collection=db['humanities-keywords-no-exact-match'])
        zp = ZipProcessor('/Users/jeremydouglass/git/preprocessing/data_zip/151550_dailynews_sayandnothumanities_2007-08-01_2007-08-30(no-exact-match).zip', hum_uploader)
        zp.process()

        deletes_comparison = db['deletes-comparison']
        comp_uploader = BatchJSONUploader(
            default_collection=db['comparison'],
            deletes_file = '_deletes.txt',
            deletes_collection=deletes_comparison,
            filter_name_cant='',
            filter_name_must='no-exact-match',
            filter_collection=deletes_comparison)
        zp = ZipProcessor('/Users/jeremydouglass/git/preprocessing/data_zip/151550_dailynews_sayandnothumanities_2007-08-01_2007-08-30(no-exact-match).zip', comp_uploader)
        zp.process()
    
runner = unittest.TextTestRunner()
result = runner.run(unittest.makeSuite(TestFuzzyZipEditor))
print(result)