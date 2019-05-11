import json
import os
import unittest

import sys
sys.path.append(".")

from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
from zipeditor import ZipEditor, zip_scanner

class TestZipEditor(unittest.TestCase):
    """Tests for the ZipEditor."""
   
    azipfile = '6742_thenewyorktimes_bodyartpre1singularhistoryorhleadartpre1singularhistory_2012-01-01_2012-12-31.zip'
    
    def test_open_close(self):
        """Test manually opening and closing a ZipEditor."""
        zed = ZipEditor(self.azipfile)
        self.assertEqual(self.azipfile, zed.file)
        self.assertIsNone(zed.getdir())
        zed.open()
        self.assertIsNotNone(zed.tmpdir.name)
        self.assertEqual(zed.tmpdir.name, zed.getdir())
        zed.close()
        self.assertIsNone(zed.getdir())

    def test_with_open_close(self):
        """Test with context for opening a ZIP file."""
        with ZipEditor(self.azipfile) as zed:
            self.assertEqual(self.azipfile, zed.file)
            self.assertIsNone(zed.getdir())
            zed.open()
            self.assertIsNotNone(zed.tmpdir.name)
            self.assertEqual(zed.tmpdir.name, zed.getdir())
        self.assertIsNone(zed.getdir())
    
    def test_open_each(self):
        """Use zip_scanner to assemble a collection of ZIP files, then test openning each."""
        zip_paths = zip_scanner(os.getcwd())
        for zip_path in zip_paths:
            with ZipEditor(zip_path) as zed:
                self.assertEqual(zip_path, zed.file)
                zed.open()
                self.assertIsNotNone(zed.tmpdir.name)
                self.assertEqual(zed.tmpdir.name, zed.getdir())
            self.assertIsNone(zed.getdir())
    
    def test_with_open_save_close(self):
        """Test with context for open, save, close of a ZIP file.
        """
        with ZipEditor(self.azipfile) as zed:
            zed.open()
            files = [entry.path for entry in os.scandir(zed.tmpdir.name) if entry.path.endswith(".json")]
            for file in files:
                with open(file, 'r+') as f:
                    data = json.load(f)
                    h = FuzzyHasher()
                    h.add_hash_to_json(data)
                    print(data['content-hash-ssdeep'])
                h.add_hash_to_json_file(file)
            zed.save(outfile=None)
            # print(files)

runner = unittest.TextTestRunner()
result = runner.run(unittest.makeSuite(TestZipEditor))
print(result)