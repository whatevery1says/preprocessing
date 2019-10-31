## mongodb import scripts

# %%capture output

print('Import humanities_keywords and reddit')

client = MongoClient('mongodb://mongo/')
db = client['we1s']

upload_list = []

hum_zip_path_list = zip_scanner_excludedirs(
    source_path='/home/jovyan/data/parsed/humanities-keywords/',
    exclude_list=[''], join=True)
hum_uploader = BatchJSONUploader2(
    default_collection=db['humanities_keywords'],
    deletes_file = '_deletes.txt',
    deletes_collection=db['deletes_humanities'],
    filter_name_cant='no-exact-match',
    filter_name_must='',
    filter_collection=db['humanities_keywords_no_exact'])
upload_list.append(hum_zip_path_list, hum_uploader)
 
rzip_path_list = zip_scanner_excludedirs(
    source_path='/home/jovyan/data/parsed/reddit/',
    exclude_list=[''], join=True)
reddit_uploader = BatchJSONUploader2(
    default_collection=db['reddit'],
    deletes_file = '_deletes.txt',
    deletes_collection=db['deletes_reddit'],
    filter_name_cant='',
    filter_name_must='',
    filter_collection=db['deletes_reddit'])
upload_list.append(rzip_path_list, reddit_uploader)

for zip_path_list, uploader in upload_list:
    for zip_path in zip_path_list:
        zp = ZipProcessor(zip_path, uploader)
        zp.process()
        # print('...processed: ', zip_path)
        # zp.open()
        # x = os.listdir(zp.getdir())
        # if '_deletes.txt' in x:
        #     print(x)
        #     print()
        # zp.close()



print('Import comparison corpus')

client = MongoClient('mongodb://mongo/')
db = client['we1s']

comp_zip_path_list = zip_scanner_excludedirs(source_path='/home/jovyan/data/parsed/comparison-corpus/',
                                        exclude_list=[''], join=True)
comp_all_uploader = BatchJSONUploader2(
    default_collection=db['comparison-not-humanities'],
    deletes_file = '_deletes.txt',
    deletes_collection=db['deletes_comparison-not-humanities'],
    filter_name_cant='',
    filter_name_must='no-exact-match',
    filter_collection=db['comparison-not-humantiies-filter'])

comp_science_uploader = BatchJSONUploader2(
    default_collection=db['comparison-sciences'],
    deletes_file = '_deletes.txt',
    deletes_collection=db['deletes_comparison-sciences'],
    filter_name_cant='no-exact-match',
    filter_name_must='',
    filter_collection=db['comparison-sciences-filter'])

# The zips are mixed together in the list, so
# two uploaders are used based on the filename:
for zip_path in comp_zip_path_list:
    if 'humanities_' in zip_path:
        zp = ZipProcessor(zip_path, comp_all_uploader)
        zp.process()
    elif 'sciences_' in zip_path:
        zp = ZipProcessor(zip_path, comp_science_uploader)
        zp.process()
    else:
        print('...missed: ', zip_path)

