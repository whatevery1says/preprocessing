"""fuzzyhasher.py."""

"""A FuzzyHasher accepts a string and returns a fuzzy hash.
It can be configured with prefilter steps for the string--
such as converting to lowercase alphanumerics only, or even
"baggifying" the words by creating an alphabetically sorted
list of all whitespace-separated tokens.

Currently only the ssdeep algorithm is supported, but it could
be extended with additional algorithms.
"""

import json
import itertools
import os
import re
import ssdeep

class FuzzyHasher:
    """Configure a fuzzy hash wrapper.
    
    Contains utility functions for working with JSON files.
    """

    def __init__(self, hash_algorithm='ssdeep',
                 source_field='content',
                 hash_field='content-hash-ssdeep',
                 prefilter='baggify,lower_alnum'):
        """Initialize the fuzzy hash wrapper object."""
        self.hash_algorithm = hash_algorithm
        self.source_field = source_field
        self.hash_field = hash_field
        self.prefilter = prefilter
        
    def add_hash_to_json(self, data, add_new=True, update_old=True):
        """Add a fuzzy hash to a JSON string.
        
        Adding new hashes
        or replacing old hashes may be separately disabled, so that
        files are only hashed when a hash is missing (for efficiency)
        or only updated (to re-hash in mixed collections).
        
        """
        if self.source_field in data:
            if self.hash_field in data:
                if update_old:
                    new_hash = self.hash(data[self.source_field])
                    if new_hash != data[self.hash_field]:
                        data[self.hash_field] = new_hash 
                        return new_hash
            else:
                if add_new:
                    new_hash = self.hash(data[self.source_field])
                    data[self.hash_field] = new_hash
                    return new_hash
        return False
        
    def add_hash_to_json_file(self, file, add_new=True, update_old=True):
        """Add a hash to a json file."""
        with open(file, 'r+') as f:
            data = json.load(f)
            change = self.add_hash_to_json(data, add_new, update_old)
            if change:
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
                return change
        return False
    
    def compare(self, hash1, hash2):
        """Compare hashes."""
        return ssdeep.compare(hash1, hash2)

    def compare_files(self, paths):
        """Compare the files."""
        hash_by_file = {}
        for path in paths:
            with open(path, 'r') as file:
                hash_string = json.load(file)['content-hash-ssdeep']
                # Get chunksize, chunk, double_chunk
                chunksize, _, _ = hash_string.split(':')
                if chunksize not in hash_by_file:
                    hash_by_file[chunksize] = {}
                hash_by_file[chunksize][hash_string] = path
                # print(chunksize, chunk, path)
        # print(hash_by_file)
        
        for chunksize, hash_list in hash_by_file.items():
            # print("\ncomparing chunksize:", chunksize, ":", len(hash_list), "examples")
            chunk_pairs = itertools.combinations([hash_entry for hash_entry in hash_list.items()], 2)
            for a, b in chunk_pairs:
                score = self.compare(a[0], b[0])
                if score > 63:
                    yield (score, a[1], b[1])

    def compare_files_in_dir(self, source_path='data'):
        """Compare the files in the directory."""
        files = [entry.path for entry in os.scandir(source_path) if entry.path.endswith(".json")]
        return self.compare_files(files)


    def hash(self, instring):
        """Hash the string."""
        for token in self.prefilter.split(','):
            if token=='alnum':
                instring = self._filter_alnum(instring)
            elif token=='baggify':
                instring = self._filter_baggify(instring)
            elif token=='lower_alnum':
                instring = self._filter_alnum(instring).lower()

        if self.hash_algorithm=='ssdeep':
            return ssdeep.hash(instring)
        
        # other algorithms: sdhash, tlsh, lzjd.
        # fuzzyhashlib contains wrappers for all of these,
        # but is python2 only.
        # another option is fuzzywuzzy
        
        else:
            return None

    def _filter_alnum(self, longstring):
        """Convert a string to an alphanumeric sequence with no spaces.
        
        Higher performance than .join(), as per
        https://stackoverflow.com/a/38799620/7207622
        """
        return re.sub(r'\W+', '', longstring)

    def _filter_baggify(self, txt):
        """Convert a string to a sorted list of tokens split on spaces."""
        return ' '.join(sorted(txt.split(' '), key=str.lower))

    # def test(self):
    #     self.hash(lower_alnum(lorem))
