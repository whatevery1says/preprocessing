## Reports: Sources


%%time
# ~1 min
# list source by article counts, descending
# NOTE: source is distinct from pub (publications)

print('Sources counts in articles collection (descending)')
client = MongoClient('mongodb://mongo/')
pipeline = [
    {'$group' : {'_id' : '$sources', 'count' : {'$sum' : 1}}},
    { '$sort' : {'count' : -1} }
]
result = client['we1s'].command('aggregate', 'humanities_keywords', pipeline=pipeline, explain=False)
for row in result['cursor']['firstBatch']:
    print(row)
    
# OUTPUT
# Sources counts in articles collection (descending)
# {'_id': ['thenewyorktimes'], 'count': 57700}
# {'_id': ['thewashingtonpost'], 'count': 37306}
# {'_id': ['thelatimes'], 'count': 34483}
# {'_id': ['chicagotribune'], 'count': 25541}
# {'_id': ['universitywire'], 'count': 24459}
# {'_id': ['theirishtimes'], 'count': 12741}
# ....




## Reports: Documents

# %%time
# # fast

client=MongoClient('mongodb://mongo/')

print("\nCount collection documents in one database\n")
report = report_collstats(db_colls(client, 'we1s'), key='count')
print_table(report)

print("\nSize collection documents in one datanbase\n")
report = report_collstats(db_colls(client, 'we1s'), key='avgObjSize')
print_table(report)

# OUTPUT
# Count collection documents in one database
# 
# count       db          coll        
# 752243      we1s        reddit      
# 508490      we1s        humanities_keywords_no_exact
# 12          we1s        comparison-not-humantiies-filter
# 418302      we1s        humanities_keywords
# 6607        we1s        comparison-sciences-filter
# 628317      we1s        comparison-sciences
# 111396      we1s        deletes_humanities
# 635495      we1s        comparison-not-humanities
# 47320       we1s        deletes_reddit
# 44114       we1s        deletes_comparison-not-humanities
# 66612       we1s        deletes_comparison-sciences
# 1           we1s        _config     
# 
# Size collection documents in one datanbase
# 
# avgObjSize  db          coll        
# 19788       we1s        reddit      
# 105391      we1s        humanities_keywords_no_exact
# 475810      we1s        comparison-not-humantiies-filter
# 137407      we1s        humanities_keywords
# 61186       we1s        comparison-sciences-filter
# 126635      we1s        comparison-sciences
# 112806      we1s        deletes_humanities
# 110219      we1s        comparison-not-humanities
# 23357       we1s        deletes_reddit
# 107897      we1s        deletes_comparison-not-humanities
# 116395      we1s        deletes_comparison-sciences
# 105650      we1s        _config 


## Report: Documents per collection

# %%time
# # fast

client=MongoClient('mongodb://mongo/')

print("\nCount collection documents in each db\n")
report = report_collstats(client_colls(client), key='count')
print_table(report)

# DEPRECATED
# print("Count documents in each db collection\n")
# mc = MongoCounter(client=MongoClient('mongodb://mongo/'))
# mc.count_docs_report()

# # DEPRECATED
# # list records in all collections
# d = dict((db, [collection for collection in client[db].list_collection_names()])
#              for db in client.list_database_names())
# for db in d:
#     for coll in d[db]:
#         # print(db, coll)
#         print((client[db].command("collstats", coll))['count'], db, coll)

# OUTPUT:
#
# Count collection documents in each db
# 
# count       db          coll        
# 1298        Sources     Sources     
# 1           admin       system.version
# 1           app         apps        
# 0           app         streams     
# 1           app         metadata    
# 240         app         deployments 
# 0           app         drafts      
# 2           auth        passwords   
# 10          auth        devices     
# 1           auth        groups      
# 0           auth        pushMessages
# 95          auth        refreshTokens
# 0           auth        apiKeys     
# 2           auth        users       
# 26          config      system.sessions
# 0           events      unordered_queue
# 1           events      counters    
# 1           events      ordered_queue
# 0           hosting     assets      
# 0           hosting     usage       
# 80          local       startup_log 
# 664         log         log         
# 0           metadata    settings    
# 1           metadata    dashboards  
# 1           metadata    items       
# 16          metadata    datasources 
# 1           metadata    users       
# 752243      we1s        reddit      
# 508490      we1s        humanities_keywords_no_exact
# 12          we1s        comparison-not-humantiies-filter
# 418302      we1s        humanities_keywords
# 6607        we1s        comparison-sciences-filter
# 628317      we1s        comparison-sciences
# 111396      we1s        deletes_humanities
# 635495      we1s        comparison-not-humanities
# 47320       we1s        deletes_reddit
# 44114       we1s        deletes_comparison-not-humanities
# 66612       we1s        deletes_comparison-sciences
# 1           we1s        _config     
# 0           we1s2018    Sources     
# 548329      we1s2018    Corpus      
# 1           we1s2018    testcollection


# Report: Documents across collections

# %%time
# # fast

client=MongoClient('mongodb://mongo/')

print("\nManipulate collection documents report as data\n")
report = report_collstats(client_colls(client), key='count', header=False)
s = sum(row[0] for row in report)
print('Documents across collections:')
print(s)

# OUTPUT:
#
# Manipulate collection documents report as data
# Documents across collections:
# 3769681



