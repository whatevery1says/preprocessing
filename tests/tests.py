import json
import os
import unittest

import sys
sys.path.append(".")

from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
from libs.zipeditor.zipeditor import ZipEditor, zip_scanner

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

runner = unittest.TextTestRunner()
result = runner.run(unittest.makeSuite(TestFuzzyZipEditor))
print(result)