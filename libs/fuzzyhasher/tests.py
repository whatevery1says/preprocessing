import os
import unittest

from fuzzyhasher import FuzzyHasher

class TestFuzzyHasher(unittest.TestCase):
    """Tests for the FuzzyHasher."""
   
    lorem='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?'
    fhash_bag_al='12:9fdNCJJf2y6QABqwE69VVtfnXDH8pEAmytsqgL8PzFXq0BHQBC7Nz73fY9FLFPu:pvCX2NQx4nnXDH8pEADCqgLGztq0BHQI'
    fhash_al='12:DX9BFsdXAVIEqan1HWthb9RjOk3MVMNJbpY+dU6sNMHL1tMfDSc/W2BJBbDQYjM:ZBFsNA2ZzFMmbArHnTDE'
    
    def test_hash(self):
        fhr = FuzzyHasher(prefilter='baggify,lower_alnum')
        print(fhr._filter_baggify(self.lorem))
        hsh = fhr.hash(self.lorem)
        print(hsh)
        self.assertEqual(hsh, self.fhash_bag_al)

    def test_add_hash_to_json_files(self):
        source_path = 'data2'
        paths = [entry.path for entry in os.scandir(source_path) if entry.path.endswith(".json")]
        fhr = FuzzyHasher(source_field='content_scrubbed')
        for path in paths:
            fhr.add_hash_to_json_file(path)

    def test_xcompare(self):
        fhr = FuzzyHasher(source_field='content_scrubbed')
        results = fhr.compare_files_in_dir('data2')
        for result in results:
            print(result)


    # def test_xcompare(self):
    #     source_path = 'data2'
    #     paths = [entry.path for entry in os.scandir(source_path) if entry.path.endswith(".json")]
    #     hash_by_file = {}
    #     for path in paths:
    #         with open(path, 'r') as file:
    #             hash_string = json.load(file)['content-hash-ssdeep']
    #             chunksize, chunk, double_chunk = hash_string.split(':')
    #             if chunksize not in hash_by_file:
    #                 hash_by_file[chunksize] = {}
    #             hash_by_file[chunksize][hash_string] = path
    #             # print(chunksize, chunk, path)
    #     # print(hash_by_file)
    #
    #     for chunksize, hash_list in hash_by_file.items():
    #         print("\ncomparing chunksize:", chunksize, ":", len(hash_list), "examples")
    #         chunk_pairs = itertools.combinations([hash_entry for hash_entry in hash_list.items()], 2)
    #         for a, b in chunk_pairs:
    #             score = ssdeep.compare(a[0], b[0])
    #             if score > 63:
    #                 print(score, a[1], b[1])




        # print(sorted(hash_by_file))
        # json_pairs = itertools.combinations(paths, 2)
        # for a, b in json_pairs:
        #     with open(a, 'r') as file1, open(b, 'r') as file2:
        #         data1 = json.load(file1)['content-hash-ssdeep']
        #         data2 = json.load(file2)['content-hash-ssdeep']
        #         score = ssdeep.compare(data1, data2)
        #         if score > 63:
        #             print(a, b, score)
        # for path in paths:
        #     with open(path, 'r+') as f:
        #         data = json.load(f)
        #         add_hash_to_json(data)
        #         print(data['content-hash-ssdeep'])
        #



runner = unittest.TextTestRunner()
result = runner.run(unittest.makeSuite(TestFuzzyHasher))
print(result)