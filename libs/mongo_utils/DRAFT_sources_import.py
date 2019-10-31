## sources

print('Import csv to mongodb sources, aliases\n')
client=MongoClient('mongodb://mongo/')
sp = SourcesProcessor(client=MongoClient('mongodb://mongo/'),
                      file_path='../sources_master.csv',
                      source_path=['Sources','Sources'],
                      aliases_path=['Sources','config','source_aliases'])
print(sp)
sp.get_csv_put_mongo()
print('aliases:', len(sp.aliases))
print('source_docs:', len(sp.source_docs))
print('csv_parse_log errors:', len(sp.csv_parse_log))
# view errors:
# print('\n'.join(sp.csv_parse_log))

print('Load sources, aliases from mongodb\n')

sp.clear()

print('source_docs:', len(sp.source_docs))
sp.get_mongo_source_docs()
print('source_docs:', len(sp.source_docs))

print('aliases:', len(sp.aliases))
sp.get_mongo_aliases()
print('aliases:', len(sp.aliases))