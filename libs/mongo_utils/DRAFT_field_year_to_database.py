## Adding Year Field to Database

%%time
## iterate over a collection, and add a pub_year int field for
## any record with a pub_date field

## on humanities_keywords w/out projection
## Wall time: 35min
## comparison-not-humanities w/ projection
## Wall time: 19min 42s
## comparison-sciences
## 


client = MongoClient('mongodb://mongo/')
db = client['we1s']
corpus = db['Corpus']
# coll = db['humanities_keywords'] # 'test'
# coll = db['comparison-not-humanities'] # 'test'
coll = db['comparison-sciences'] # 'test'
counter = 0
for doc in coll.find({"pub_date":{"$exists": True}}, { '_id':1, 'pub_date':1}):
    pub_year_str = doc['pub_date'][0:4]
    if(len(pub_year_str)==4 and pub_year_str.isdigit()):
        pub_year = int(pub_year_str)
        coll.update_one({'_id': doc['_id']},{'$set': {'pub_year': pub_year }}, upsert=False)
        if(counter%100==0):
            print(pub_year, end=' ')
    counter += 1
print('\n')

