## Article rewriting


### setup

print('Setup ArticleProcessor with SourcesProcessor')
client=MongoClient('mongodb://mongo/')
sp = SourcesProcessor(client=MongoClient('mongodb://mongo/'),
                      file_path='../sources_master.csv',
                      source_path=['Sources','Sources'],
                      aliases_path=['Sources','config','source_aliases'])
ap = ArticleProcessor(sp)


### display sample article rewrite (Jupyter)

print('Rewrite documents in memory and preview in-memory, no mongo update')

# select data
coll = client['we1s']['deletes_humanities']
docs = coll.aggregate([{ '$sample': { 'size': 4 } }])

# preview config
pop_list = ['features','language_model','content-unscrubbed']
trim_dict={'content':500, 'attachment_id': 30, 'doc_id':40, 'metapath':40, 'content-hash-ssdeep': 30, 'name':40}

# display with single table style
data = []
data.append(('before (preview)', 'after (preview)'))
for doc in docs:
    before, after = ap.json_update_previews(doc, pop_list=pop_list, trim_dict=trim_dict, width=60)
    # the full `doc` has been changed at this point, could be written.
    data.append((before,after))
ap.display_ipython_table(data) 

# # ...or display with floating table rows style
# for doc in docs:
#     before, after = ap.json_update_previews(doc, pop_list=pop_list, trim_dict=trim_dict, width=60)
#     # the full `doc` has been changed at this point, could be written.
#     ap.display_ipython_table([(before,after)]) 



## DISABLED

## From-mongo rewrite w/out update -- could instead rewrite before insert

# # def rewrite_docs(aliases, docs):
# for doc in docs: 
#     rewrite(doc, aliases)
#     print(doc_preview(doc, pop_list=['features','language_model','content-unscrubbed'], trim_dict={'content':500}))

# # def rewrite_mongo_coll(aliases, coll, docs):
# for doc in docs: 
#     rewrite(doc)
#     coll.replace_one({'_id':doc['_id']}, doc, upsert=True)
#     print(doc_preview(doc, pop_list=['features','language_model','content-unscrubbed'], trim_dict={'content':500})

# aliases = client['Sources']['config'].find_one({'_id':'source_aliases'})['aliases']
# coll = client['we1s']['deletes_humanities']
# docs = coll.aggregate([{ '$sample': { 'size': 2 } }])
# rewrite_mongo_coll(aliases, coll, docs)

# docs = client['we1s']['deletes_humanities'].aggregate([{ '$sample': { 'size': 2 } }])
# # docs = client['we1s']['deletes_humanities'].collection.find({})

# OUTPUT:
# rewrite: 5d3acd40f123b8357f488425
# { '_id': ObjectId('5d3acd40f123b8357f488425'),
#   'api_data_provider': 'LexisNexis',
#   'api_software': 'we1s-collector',
#   'attachment_id': 'LNCDBE032A334E6199C0814D4A55AE10E64CD13C619E192CC1',
#   'content': 'She has already penned poems in honour of the last British '
#              'soldiers to fight in the First World War, the wedding of Prince '
#              'William and Kate Middleton, the MPs expenses scandal and an '
# ...

