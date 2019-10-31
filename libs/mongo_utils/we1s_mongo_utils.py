"""we1s_mongo_utils.py
WE1S-specific importing and updating tools for pymongo and mongodb.
"""

import copy
import csv
import json
import os
import pymongo
import pprint

pp = pprint.PrettyPrinter(indent=2, compact=False)

def doc_preview(doc, pop_list=None, trim_dict=None, trim_mark='...', object=False, width=None):
    preview = copy.deepcopy(doc)
    if pop_list:
        for key in pop_list:
            if key in preview:
                preview.pop(key)
    if trim_dict:
        for key, value in trim_dict.items():
            if key in preview:
                if len(key) <= value and len(key) > len(trim_mark):
                    preview[key] = ''.join([preview[key][0:value-len(trim_mark)], trim_mark])
    if object:
        return preview
    if width: 
        return pprint.pformat(preview, width=width)
    return pp.pformat(preview)

class SourcesProcessor:
    """Documents the pipeline for populating mongodb source docs
    and aliases from a csv spreadsheet.
    
    Use:
        csv_to_mongo(client, filepath)
        
    Internal class methods are stages in the pipeline.
    """

    def __init__(self,
                 client=MongoClient('mongodb://mongo/'),
                 file_path='../sources_master.csv',
                 source_path=['Sources','Sources'],
                 aliases_path=['Sources','config','source_aliases']):
        self.client = client
        self.file_path = file_path
        self.source_path = source_path
        self.aliases_path = aliases_path
        self.clear()

    def clear(self):
        self.aliases = {}
        self.source_docs = {}
    
    def get_csv_put_mongo(self):
        self.get_csv()
        self.put_mongo_aliases()
        self.put_mongo_source_docs()

    def get_csv(self):
        """Given a DictReader, returns sources docs and an aliases lookup as data structures.
        
        The data format is:
        title,name,canonical_title,tags1,tags2,tags3,tags4,tags5,tags6,country,language
        
        mockup of a Source manifest:
        {
            "name": "advance-titan-university-of-wisconsin-oshkosh",
            "metapath": "Sources",
            "namespace": "we1s2.0",
            "title": "Advance-Titan: University of Wisconsin - Oshkosh",
            "country": "US",
            "language": "en",
            "tags": ["region/US/Midwest", "education/funding/US public college"],
            "collection_identifiers": ["Advance", "Advance-Titan", "Advance-Titan: University of Wisconsin - Oshkosh"]
        }
        """

        self.aliases = {} # alias-to-name lookup entries
        self.source_docs = {}  # sources docs
        self.csv_parse_log = []
        name_prev = ''
        csvfile = open(self.file_path, 'r')
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            # build source_name_aliases
            akey = mdbkey_encode(row['alias'])
            dkey = row['name'].strip()
            if akey and akey not in self.aliases:
                self.aliases[akey] = dkey
            else:
                self.csv_parse_log.append("duplicate key '{0}' found: '{1}'".format(akey, row['name'].strip()))
                # raise ValueError("duplicate key '{0}' found".format(akey))
    
            # build source_docs
            if dkey in self.source_docs:
                # if name is a repeat, add an alias and continue
                self.source_docs[dkey]['aliases'].append(row['alias'].strip())
            else:
                # if source name is new, create
                # this is an explicit add -- new named columns in the sheet won't be imported
                self.source_docs[dkey] = {}
                self.source_docs[dkey]['_id'] = dkey # This creates a problem in Manager pagination
                self.source_docs[dkey]['name'] = dkey
                self.source_docs[dkey]['country'] = row['country']
                self.source_docs[dkey]['language'] = row['language']
                self.source_docs[dkey]['metapath'] = 'Sources'
                self.source_docs[dkey]['namespace'] = 'we1s2.0'
                self.source_docs[dkey]['title'] = row['canonical_title'].strip()
                tags = [row['tags1'],row['tags2'],row['tags3'],row['tags4'],row['tags5'],row['tags6']]
                self.source_docs[dkey]['tags'] = [x for x in tags if x]
                self.source_docs[dkey]['aliases'] = [row['alias'].strip()]
    
    def get_mongo_aliases(self):
        """get aliases from db"""
        ap = self.aliases_path
        self.aliases = self.client[ap[0]][ap[1]].find_one({'_id' : ap[2]})['aliases']

    def get_mongo_source_docs(self):
        sp = self.source_path
        results = self.client[sp[0]][sp[1]].find({})
        self.source_docs = {}
        for result in results:
            self.source_docs[result['_id']] = result        

    def put_mongo_aliases(self):
        """insert aliases into db as doc"""
        doc = {}
        doc['_id'] = self.aliases_path[2]
        doc['aliases'] = self.aliases
        ap = self.aliases_path
        self.client[ap[0]][ap[1]].replace_one({'_id' : ap[2]}, doc, upsert=True)

    def put_mongo_source_docs(self):
        """insert source docs into db"""
        sp = self.source_path
        for key, source_doc in self.source_docs.items():
            client[sp[0]][sp[1]].replace_one({'_id':source_doc['_id']}, source_doc, upsert=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(client={self.client}, file_path={self.file_path}, source_path={self.source_path}, aliases_path={self.aliases_path})'


class ArticleProcessor:
    """Dynamic rewriting of article data fields, particularly
    the source field and api fields.
    Relies on data from source aliases -- uploaded / retrieved with SourcesProcessor
    """
    
    def __init__(self, sources_processor):
        self.sp = sources_processor
        self.sp.get_mongo_aliases()
        self.aliases = sp.aliases
        self.source_docs = sp.source_docs

    def display_ipython_table(self, data):
        from IPython.display import display, HTML
        # css_str = '<style>body{background-color:#000000}; table{width:600px !important}; td{width:200 !important};</style>'
        css_str = '<style>td{border: 1px solid black} td{text-align:left; vertical-align:top}</style>'
        display(HTML(
            css_str + '<table><tr style>{}</tr></table>'.format(
                '</tr><tr>'.join(
                '<td><pre>{}</pre></td>'.format('</pre></td><td><pre>'.join(str(_) for _ in row)) for row in data)
            )), metadata=dict(isolated=True))

    def json_add_api_fields(self, json_data, name_hint):
        """Set json api... fields from name hint and optional
        database field. Hint may be generated by
        json_add_api_fields_guess checking the name field.
        """
        translations = {
            'LexisNexis':['we1s-collector', 'LexisNexis'],
            'LexisNexis UniversityWire':['we1s-collector', 'LexisNexis', 'UniversityWire'],
            'chomp':['chomp','chomp'],
            # 'chomp':['chomp','google.com'],
            # 'chomp':['chomp','wordpress.com'],
            'ProQuest':['ProQuest Global Newsstream','ProQuest'],
            'Global Newsstream':['ProQuest Global Newsstream','ProQuest'],
            'Global Newsstrea m':['ProQuest Global Newsstream','ProQuest'],
            'Globa l Newsstream':['ProQuest Global Newsstream','ProQuest'],
            'Global Newss tream':['ProQuest Global Newsstream','ProQuest'],
            'Ethnic NewsWatch':['ProQuest Global Newsstream', 'ProQuest','Ethnic NewsWatch'],
            'Ethnic NewsWatc h':['ProQuest Global Newsstream','ProQuest','Ethnic NewsWatch'],
            'Ethnic N ewsWatch':['ProQuest Global Newsstream','ProQuest','Ethnic NewsWatch'],
            'Ethnic NewsWatch; GenderWatch':['ProQuest Global Newsstream','ProQuest','Ethnic NewsWatch; GenderWatch'],
            'GenderWatch':['ProQuest Global Newsstream','ProQuest','GenderWatch'],
            'reddit':['reddit','reddit'],
            'Twitter':['Twitter','Twitter']
        }
        # manual dictionary
        if 'database' in json_data:
            # lookups and 
            labels = translations[json_data['database']]
        else:
            # fall back to name label
            labels = translations[name_hint]
    
        # set the fields
        if 'api_software' not in json_data:
            json_data['api_software'] = labels[0]
        if 'api_data_provider' not in json_data:
            json_data['api_data_provider'] = labels[1]
        if(len(labels)>2):
            if 'api_data_provider_channel' not in json_data:
                json_data['api_data_provider_channel'] = labels[2]
    
    def json_add_api_fields_guess(self, json_data):
        """Deduce api fields hint from name, try lookup
        and add api_fields to json.
        """
        if 'name' in json_data:
            if 'chomp' in json_data['name'].lower() :
                self.json_add_api_fields(json_data, 'chomp')
            elif 'reddit' in json_data['name'].lower():
                self.json_add_api_fields(json_data, 'reddit')
            elif 'proquest' in json_data['name'].lower():
                self.json_add_api_fields(json_data, 'ProQuest')
            elif 'twitter' in json_data['name'].lower():
                self.json_add_api_fields(json_data, 'Twitter')
            elif 'universitywire' in json_data['name'].lower():
                self.json_add_api_fields(json_data, 'LexisNexis UniversityWire')
            else:
                self.json_add_api_fields(json_data, 'LexisNexis')
    
    def json_add_source(self, json_data, aliases=None):
        """use source name aliases dict to lookup and save canonical source name.
        """
        if not aliases: aliases = self.aliases
        lookup_name = ''
        if 'name' in json_data:
            if 'chomp' in json_data['name'].lower() :
                # chomp zip:  chomp_vox_humanities_2000-01-01_2020-01-01.zip
                # chomp json: chomp_vox_humanities_2000-01-01_2020-01-01_0.json
                lookup_name = json_data['name'].split('_')[1]
            elif 'reddit' in json_data['name'].lower():
                # reddit zip:  reddit-all-the-arts-2006-2018-264.zip
                # reddit json: Reddit-The-Arts-All-2006-2018_180.json
                lookup_name = 'Reddit'
            elif 'proquest' in json_data['name'].lower():
                # proquest has no standard format
                # proquest  zip: proquest_thewallstreetjournal_humanities_1984_1989.zip
                # proquest json: proquest_thewallstreetjournal_humanities_1984_1989_001_.json
                if 'thewallstreetjournal' in json_data['name'].lower():
                    # proquest-wallstreet exception
                    lookup_name = 'thewallstreetjournal'
                else:
                    lookup_name = json_data['pub']
            elif 'universitywire' in json_data['name'].lower():
                # LN University Wire
                # zip: 172244_universitywire_bodypluralhumanitiesorhleadpluralhumanities_2014-01-01_2014-12-31.zip
                # json: 172244_172244_universitywire_bodypluralhumanitiesorhleadpluralhumanities_2014-01-01_2014-12-31_16_0_0.json
                lookup_name = json_data['pub']
            else:
                # LexisNexis default
                # zip: 8006_thelatimes_bodypluralhumanitiesorhleadpluralhumanities_2011-01-01_2011-12-31.zip
                # json: 8006_8006_thelatimes_bodypluralhumanitiesorhleadpluralhumanities_2011-01-01_2011-12-31_55_0_0.json
                lookup_name = json_data['name'].split('_')[2]
        source_name = aliases[mdbkey_encode(lookup_name)]
        # print('cn:', canonical_name, type(canonical_name))
        if 'sources' in json_data:
            json_data.pop('sources')
        json_data['source'] = source_name

    def json_update(self, doc, aliases=None):
        """Given an in-memory doc, do an in-memory rewrite
        based on:
            add_source
            add_api_fields_guess
        This does not add/update the document to a database.
        """
        if not aliases: aliases = self.aliases
        # print('rewrite:', doc['_id'])
        self.json_add_source(doc, aliases)
        self.json_add_api_fields_guess(doc)

    def json_update_previews(self, doc, pop_list=None, trim_dict=None, width=None):
        """Changes the in-memory doc with json_update,
        returns two doc_previews with pretty printing: before and after.
        """
        before_prev = doc_preview(doc, pop_list=pop_list, trim_dict=trim_dict, width=width)
        self.json_update(doc)
        after_prev = doc_preview(doc, pop_list=pop_list, trim_dict=trim_dict, width=width)
        return before_prev, after_prev

    def mongo_replace_docs(self, docs, collection):
        for doc in docs:
            self.json_update(doc)
            collection.replace_one({'_id': doc['_id']}, doc, upsert=False)
    
    def mongo_update_docs(self, docs, collection):
        for doc in docs:
            self.mongo_update_doc(doc, collection)
    
    def mongo_update_doc(self, doc, collection):
        self.json_update(doc)
        update_command = {'$set': {'api_data_provider': doc['api_data_provider'].strip(),
                                   'api_software': doc['api_software'].strip(),
                                   'source': doc['source'].strip()
                                  },
                          '$unset': { 'sources' : "", 'length' : "" }}
        if 'api_data_provider_channel' in doc:
            update_command.setdefault('$set', {})
            update_command['$set']['api_data_provider_channel'] = doc['api_data_provider_channel']            
        if 'api_data_provider' in doc and 'LexisNexis' in doc['api_data_provider']:
            update_command.setdefault('$rename', {})
            update_command['$rename']['doc_id'] = 'ln_doc_id'
            update_command['$rename']['attachment_id'] = 'ln_attachment_id'
        
        updated = collection.find_one_and_update({'_id': doc['_id']},
                                                 update_command,
                                                 return_document=pymongo.ReturnDocument.AFTER,
                                                 upsert=False)
        return updated
