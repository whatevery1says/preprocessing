
client['we1s']['humanities_keywords'].create_index([('sources', pymongo.ASCENDING)])
client['we1s']['comparison-not-humanities'].create_index([('sources', pymongo.ASCENDING)])
client['we1s']['comparison-sciences'].create_index([('sources', pymongo.ASCENDING)])
client['we1s']['humanities_keywords'].create_index([('pub_year', pymongo.ASCENDING)])
client['we1s']['comparison-not-humanities'].create_index([('pub_year', pymongo.ASCENDING)])
client['we1s']['comparison-sciences'].create_index([('pub_year', pymongo.ASCENDING)])

