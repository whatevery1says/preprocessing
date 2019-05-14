"""zipeditor.py."""

import os
import shutil
import tempfile
import zipfile

def zip_scanner(source_path=''):
    """Return a list of zip files from a source directory."""
    if not source_path:
        source_path = os.getcwd()
    return [entry.path for entry in os.scandir(source_path) if entry.path.endswith(".zip")]

class ZipEditor:
    """Provide an editing context for a ZIP file.
    
    `open()` extracts a ZIP file
    into a temporary directory and returns the directory. After modification,
    `save()` replaces the ZIP file with a newly zipped copy of the temp directory.
    Close cleans up and removes the temp contents -- or use `with` for auto-cleanup.
    
    This wrapper exists because editing files inside a ZIP is not supported in the
    standard zipfile library. This approach does not file lock the zip during editing,
    but it should handle very large zip files better than in-memory.

    """
    
    def __init__(self, file):
        """Create a new ZipEditor based on a file.

        Args:
            file: a ZIP file. Can be a path to a file (a string), a file-like object, or a path-like object.

        """
        self.file = file
        self.tmpdir = None

    def __del__(self):
        """On garbage collect, clean up."""
        self._close()

    def __enter__(self):
        """Enter context using `with`."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """On context exit, clean up."""
        self._close()

    def close(self):
        """Close and remove temp directory."""
        was_open = self._close()
        if not was_open:
            raise IOError("Zip file not open.")

    def getdir(self):
        """Return the temp working directory for the unpacked zip (if it exists)."""
        if self.tmpdir:
            return self.tmpdir.name
        else:
            return None

    def open(self):
        """Unpack zip into temp directory for editing."""
        if not self.tmpdir:
            self.tmpdir = tempfile.TemporaryDirectory()
            zip_obj = zipfile.ZipFile(self.file, 'r')
            zip_obj.extractall(path=self.tmpdir.name, members=None, pwd=None)
            return self.tmpdir.name
        else:
            raise IOError("Zip file already open.")

    def save(self, outfile=None):
        """Save the file.

        !! Appears to create a .zip.zip !!
        https://stackoverflow.com/q/1855095/7207622

        """
        if not outfile:
            outfile = self.file
        if self.tmpdir:
            # zip_obj = zipfile.ZipFile(outfile, 'r')
            # print("outfile:", outfile, "tmpdir:", self.tmpdir.name)
            shutil.make_archive(os.path.splitext(outfile)[0], 'zip', self.tmpdir.name)
        else:
            raise IOError("Zip file not open.")
 
    def _close(self):
        """Close and remove temp directory."""
        if self.tmpdir:
            self.tmpdir.cleanup()
            self.tmpdir = None
            return True
        return False    
