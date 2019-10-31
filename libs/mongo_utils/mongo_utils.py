"""mongo_utils.py
General purpose tools for working with pymongo and mongodb.
"""

from collections import Counter
from datetime import datetime
import json
import os
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError, InvalidDocument
import pprint
pp = pprint.PrettyPrinter(indent=2, compact=False)

# import sys
# sys.path.insert(0, '/home/jovyan/utils/preprocessing/')
# from libs.fuzzyhasher.fuzzyhasher import FuzzyHasher
# from libs.zipeditor.zipeditor import ZipEditor, zip_scanner, zip_scanner_excludedirs, ZipProcessor
# from we1s_utils.ziputils import BatchJSONUploader

# filter = {"name": {"$regex": r"^(?!system\.)"}}

# def _tabulate_row(*row):
#     return ''.join(str(word).ljust(12) for word in row)



##############################
##  mongodb doc generators  ##
##############################
## these two (client_colls and db_colls)
## and their dependents might be refactored
## -- as it turns out, the database and client
## are retrievable from the collection object,
## so interfaces to collection level function
## could be simplified.
##
## client = MongoClient('mongodb://mongo/')
## db = client['we1s']
## coll = db['deletes_humanities']
##
## print(coll)
## print(coll.name)
## print(coll.database)
## print(coll.database.name)
## print(coll.database.client)
##
## OUTPUT:
## Collection(Database(MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True), 'we1s'), 'deletes_humanities')
## deletes_humanities
## Database(MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True), 'we1s')
## we1s
## MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True)
## Database(MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True), 'name')

def client_colls(client, filter=None):
    """All collections across all databases--generator."""
    d = dict((db, [collection for collection in client[db].list_collection_names(filter=filter)])
             for db in client.list_database_names())
    for db in d:
        for coll in d[db]:
            yield client, db, coll
            # yield coll
        
def db_colls(client, db, filter=None):
    """All collections in a database--generator."""
    db_coll_list = [collection for collection in client[db].list_collection_names(filter=filter)]
    for coll in db_coll_list:
        yield client, db, coll
        # yield coll



def mdbkey_decode(key):
    """Decode encoded mongodb key to recover original string."""
    return key.replace("\\u002e", ".").replace("\\u0024", "\$").replace("\\\\", "\\")

def mdbkey_encode(key):
    """Encode key field with . or $ to be valid mongodb key."""
    return key.replace("\\", "\\\\").replace(".", "\\u002e").replace("\$", "\\u0024")

def mdbkey_strip(key):
    """Strip . or $ to enforce valid mongodb key."""
    return key.replace(".", "").replace("$", "")

def print_doc(doc, pop_list=None, trim_dict=None):
    """Cleans up verbose mongodb JSON documents for preview
    using a list of top-level fields to pop or trim.
    """
    if pop_list:
        for key in pop_list:
            if key in doc:
                doc.pop(key)
    if trim_dict:
        for key, value in trim_dict.items():
            if key in doc:
                doc[key] = doc[key][0:value]
    pp.pprint(doc)


def print_query(query, style='pp'):
    """Convenience method for displaying pymongo
    queries in readable formats. Three styles:
    PrettyPrinter, json.dumps(), or print().
    
    Examples:
        >>> query = {'$or': [{'name': {'$regex': '.*liberal.*'}}, {'name': {'$regex': '.*humanities.*'}}]}
        >>> print_query(query)
        {   '$or': [   {'name': {'$regex': '.*liberal.*'}},
                       {'name': {'$regex': '.*humanities.*'}}]}

        >>> print_query(query, style=None)
        {'$or': [{'name': {'$regex': '.*liberal.*'}}, {'name': {'$regex': '.*humanities.*'}}]}

        >>> print_query(query, style='json')
        {
            "$or": [
                {
                    "name": {
                        "$regex": ".*liberal.*"
                    }
                },
                {
                    "name": {
                        "$regex": ".*humanities.*"
                    }
                }
            ]
        }
    """
    if style=='pp':
        # pprint adds linebreaks and indents, yet stays compact
        pp.pprint(query)
    elif style=='json':
        # json can also be used to print nested dict/lists
        # in a more articulated indented outline form
        print(json.dumps(query, sort_keys=True, indent=4))
    else:
        # pymongo queries are python dicts of dicts (or lists of dicts)
        # however, these nested lines may be hard to read        
        print(query)

def _test_print_query():
    """Test three output formats"""
    print('Display a mongodb query in three different print formats.')
    query = {'$or': [{'name': {'$regex': '.*liberal.*'}}, {'name': {'$regex': '.*humanities.*'}}]}
    print('----------')
    print_query(query, style='None')
    print('----------')
    print_query(query)
    print('----------')
    print_query(query, style='json')

def print_table(rows):
    for row in rows:
        print(''.join(str(word).ljust(12) for word in row))

def print_SON(son):
    if son:
        print(index.to_dict())

def report_aggregate(coll_list, pipeline):
    """
    pipeline_pub = [
        {'$group' : {'_id' : '$pub', 'count' : {'$sum' : 1}}},
        { '$sort' : {'count' : -1} }
    ]
    pipeline_term = [
        {'$group' : {'_id' : '$term', 'count' : {'$sum' : 1}}},
        { '$sort' : {'count' : -1} }
    ]
    """
    report = []
    for client, db, coll in coll_list:
        result = client[db].command('aggregate', coll, pipeline=pipeline, explain=False)
        for row in result:
            if row:
                report.append(json.dumps(row, sort_keys=True, indent=2))
    return report

def report_collstats(coll_list, key='count', header=True):
    """Return a stat (e.g. document count) for each mongodb
    collection list.
    May be passed a generator such as client_colls or db_colls.
    Pretty-print with print_table().

    Examples:
        >>> report_collstats((client, 'we1s', 'reddit'))
        count       db          coll      
        12345       we1s        reddit    

        >>> report_collstats(db_colls(client, 'we1s'), key='avgObjSize')
        avgObjSize  db          coll      
        19788       we1s        reddit    
        105391      we1s        humanities_keywords_no_exact

    Args:
        coll_list (tuple): (client, db_name, coll_name)
        key (str): the stat to report.
        header (bool): Include column headers in output

    Returns:
        A list of the key value for each db.collection:
        [(key, db, coll),
         (key, db, coll),
         (key, db, coll)]
    """

    report = []
    for client, db, coll in coll_list:
        if key:
            value = client[db].command("collstats", coll)[key]
        else:
            value = client[db].command("collstats", coll)
        report.append((value, db, coll))
    if report:
        if header:
            report.insert(0, (key, 'db', 'coll'))
        return report

def report_indexes(coll_list):
    """Return all indexes for each mongodb collection in a list.
    May be passed a generator such as client_colls or db_colls.
    Pretty-print with print_SON().
    
    Args:
        coll_list (tuple): (client, db_name, coll_name)

    Returns:
        A list of indexes (SON objects).
        [SON, SON, SON]
    """
    result = []
    for client, db, coll in coll_list:
        for index in client[db][coll].list_indexes():
            if index:
                result.append(index)
    return result




class MongoCounter:
    """For a mongo server or collection, build a list of FieldCounters"""

    def __init__(self, client=None, progress=None):
        self.results = []
        self.client = client
        self.progress = progress

    def _client_dbs_command(self, client, command='collstats'):
        """Loop over all dbs and all collections,
        returning command result for each collection.
        """
        d = dict((db, [collection for collection in client[db].list_collection_names()])
                     for db in client.list_database_names())
        for db in d:
            for coll in d[db]:
                # print(db, coll)
                yield client[db].command(command, coll), db, coll

    def _tabulate(self, *row):
        return ''.join(str(word).ljust(10) for word in row)

#     # DEPRECATED
#     def count_docs(self, client=None):
#         """Display document counts for all collections in all dbs.
#         e.g.
#         79 local startup_log
#         752243 we1s reddit
#         418302 we1s humanities_keywords
#         """
#         if not client: client = self.client
#         counts = self._client_dbs_command(client, command='collstats')
#         for collstats, db, coll in counts:
#             yield collstats['count'], db, coll

#     def count_docs_report(self, client=None):
#         if not client: client = self.client
#         counts = self.count_docs(client)
#         for collstats, db, coll in counts:
#             print(self._tabulate(collstats, db + '.' + coll))
            
    def count_fields_all(self,  client=None, progress=None, show_complete=True):
        if not client: client = self.client
        for db in client.list_database_names():
            self.count_fields_db(db, client, progress, show_complete)
        
    def count_fields_db(self, db, client=None, progress=None, show_complete=True):
        if not client: client = self.client
        db_colls = [collection for collection in client[db].list_collection_names()]
        for coll in db_colls:
            self.count_fields_collection(coll, db, client, progress, show_complete)
    
    def count_fields_collection(self, coll, db, client=None, progress=None, show_complete=True):
        if not client: client = self.client
        if progress==None and self.progress:
            progress=self.progress
        coll_count = client[db].command("collstats", coll)['count']
        fcounter = FieldCounter(name=db+'.'+coll + '(' + str(coll_count) + ' docs)', show_complete=show_complete)
        cursor = client[db][coll].find({})
        print(fcounter)
        for doc in cursor:
            if progress and fcounter.total !=0 and fcounter.total % progress == 0:
                print(fcounter)
            fcounter.count_fields(doc)
        # print('\n\n', '[FINAL]')
        print(fcounter.report())
        self.results.append(fcounter)

#     # DEPRECATED
#     def list_indexes(self, client=None):
#         """Loop over all dbs and all collections,
#         returning command result for each collection.
#         """
#         if not client: client = self.client
#         d = dict((db, [collection for collection in client[db].list_collection_names()])
#                      for db in client.list_database_names())
#         for db in d:
#             for coll in d[db]:
#                 for index in client[db][coll].list_indexes():
#                     print(index, db, coll)

    def __str__(self):
        return '\n'.join([result for result in self.results])


class FieldCounter:
    """Build counters of dictionary fields.
    Useful for surveying mongodb collections for presence/absence of keys across documents.
    Keeps two fields counters:
    
    -  counter: present fields with value
    -  counter_empties: present fields that are false (None, 0, '', false, etc.)
    ...and:
    -  total: number of documents counted
    
    Supports includes and excludes -- lists of fields to include or ignore.
    If includes are defined then only includes will be counted -- unless they
    are subsequently filtered by the excludes list.
    """

    def __init__(self, name='', show_complete=True, includes=None, excludes=None):
        self.name = name
        self.show_complete = show_complete
        self.includes = includes
        self.excludes = excludes
        self.clear()

    def _tabulate(self, *row):
        return ''.join(str(word).ljust(10) for word in row)
    
    def clear(self):
        self.counter = Counter()
        self.counter_empties = Counter()
        self.total = 0

    def count_collection(self, docs, includes=None, excludes=None):
        if not includes: includes = self.includes
        if not excludes: excludes = self.excludes
        for doc in docs:
            yield self.count_fields(doc, includes, excludes)

    def count_fields(self, doc, includes=None, excludes=None):
        """"""
        if not includes: includes = self.includes
        if not excludes: excludes = self.excludes
        for key, value in doc.items():
            if (not includes or key in includes) and (not excludes or key not in excludes):
                if value:
                    self.counter[key] += 1
                else:
                    self.counter_empties[key] += 1
        self.total+=1
        return doc, self.total

    def report(self, header=False):
        result = ''
        if header:
            result = self.__str__()
        if self.total > 0:
            colnames = self._tabulate('found', 'empties', 'missing', 'key')
            emptycount = 0
            entries = ''
            for key, value in sorted(self.counter.items()):
                if value != self.total:
                    emptycount = self.counter_empties.get(key, 0)
                if self.show_complete or value != self.total:
                    entries += self._tabulate(value, emptycount, self.total-value, key) + '\n'
            if entries:
                result = '\n'.join([result, colnames, entries])
                result += self._tabulate(str(self.total), 'counted') + '\n'
            else:
                result += '[no fields empty/missing]\n'
        else:
            result += '[no docs]\n'
        return result
    
    def __str__(self):
        return self.name

# STRIP FIELD WHITESPACE

def mongo_coll_field_update(coll, field, func):
    """Given a collection, updates each doc with the field,
    changing it to using the lambda function."""
    hits = 0
    for doc in coll.find({field: {'$exists': True, '$ne': []}}, {field:1}):
        if mongo_field_update(coll, doc, field, func):
            hits += 1
    return hits

def mongo_field_update(coll, doc, field, func):
    """Given a doc, changes a field and updates it in mongodb."""
    if field_update(doc, field, func):
        # print('*', end='')
        coll.update_one({'_id': doc['_id']},
                        {'$set': {field: doc[field]} },
                        upsert=False)
        return True
    return False

def field_update(doc, field, func):
    """Takes a doc, field name, and lambda function for the field.
    Changes the field in place and returns True if updated.
    """
    if field in doc and doc[field]:
        val = func(doc[field])
        if doc[field] != val:
            doc[field] = val
            return True
    return False

def func_strip(x):
    """Many fields have leading and trailing spaces,
    leading to e.g. four different "The New York Times".
    for a collection, iterate over all pub fields and,
    if there are leading or trailing spaces, strip.
    this should really be part of a pre-import validator.
    """
    return x.strip()
    # this could also be passed without a function as:
    #   lambda x: x.strip()

    
#
#  DEPRECATED 
#
#  def strip_field(db, collection, field):
#     """Many fields have leading and trailing spaces,
#     leading to e.g. four different "The New York Times".
#     for a collection, iterate over all pub fields and,
#     if there are leading or trailing spaces, strip.
#     this should really be part of a pre-import validator.
#     """
#     test_collect = client['we1s']['deletes_humanities']
#     hits = 0
#     fixed = 0
#     for doc in test_collect.find({'pub': {'$exists': True, '$ne': []}}, {'pub':1}):
#         hits += 1
#         if 'pub' in doc and doc['pub']:
#             if doc['pub'] != doc['pub'].strip():
#                 fixed += 1
#                 test_collect.update_one({'_id': doc['_id']},
#                                     {'$set': {'pub': doc['pub'].strip()} },
#                                     upsert=False)
#     print('hits:  ', hits)
#     print('fixed: ', fixed)
# 
# strip_field(1, 2, 3)
