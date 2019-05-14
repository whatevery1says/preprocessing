"""preprocess.py"""

# Python imports
import csv  
import json  
import os
import nltk
import pandas as pd
import re
import time
import unicodedata
# import fire
import spacy
from spacy.symbols import ORTH, LEMMA, POS, TAG
from spacy.tokenizer import Tokenizer
from collections import Counter
from ftfy import fix_text
from nltk.stem.porter import PorterStemmer  
from nltk.stem.snowball import SnowballStemmer
from nltk.util import ngrams


## CONSTANTS
LINEBREAK_REGEX = re.compile(r'((\r\n)|[\n\v])+')
NONBREAKING_SPACE_REGEX = re.compile(r'(?!\n)\s+')
PREFIX_RE = re.compile(r'''^[\[\]\("'\.,;:-]''')
SUFFIX_RE = re.compile(r'''[\[\]\)"'\.,;:-]$''')
INFIX_RE = re.compile(r'''[-~]''')
SIMPLE_URL_RE = re.compile(r'''^https?://''')



# The Document class
class Document:
    """Model a document's features.

    Parameters:
    - manifest_dir: the path to the manifest directory
    - manifest_file: the name of the manifest file.
    - content_property: the name of the property from which to extract the content
    Returns a dataframe.
    """
    
    def __init__(self, manifest_dir, manifest_file, content_property, model, **kwargs):
        """Initialize the object."""
        self.nlp = model
        self.manifest_filepath = os.path.join(manifest_dir, manifest_file)
        self.manifest_dict = self._read_manifest()
        # Hack to deal the inconsistencies in our current collection
        special_cases = ['content', 'content_scrubbed', 'content_unscrubbed']
        # Look for some user-supplied content property
        if content_property in self.manifest_dict and content_property not in special_cases:
            pass
        # Transfer `content-unscrubbed` to `content`
        elif 'content-unscrubbed' in self.manifest_dict:
            self.manifest_dict['content'] = self.manifest_dict['content-unscrubbed']
            del self.manifest_dict['content-unscrubbed']
        # Transfer `content_scrubbed` to `content`
        elif 'content_scrubbed' in self.manifest_dict:
            self.manifest_dict['content'] = self.manifest_dict['content_scrubbed']
            del self.manifest_dict['content_scrubbed']
        # Otherwise, assume the `content` property
        else:
            content_property = 'content'
        self.doc_string = self.scrub(self._get_docstring(content_property))
        self.content = self.nlp(self.doc_string)
        # self.options = kwargs['kwargs']
        self.options = kwargs
        # Re-do this to deserialise a list of lists.
        if 'features' in self.manifest_dict:
            self.features = self.get_features()
            # self.features = self.deserialize(json.dumps(self.manifest_dict['features']))
        else:
            self.features = self.get_features()

    def _remove_accents(self, text, method='unicode'):
        """Remove accents from any accented unicode characters in a string.

        Either transforms them into ascii equivalents or removes them entirely.
        Parameters:
        - text (str): raw text
        - method ({'unicode', 'ascii'}): if 'unicode', remove accented
            char for any unicode symbol with a direct ASCII equivalent; if 'ascii',
            remove accented char for any unicode symbol.
            NB: the 'ascii' method is notably faster but less effective than 'unicode'.
        Returns:
            str
        Raises:
            ValueError: if ``method`` is not in {'unicode', 'ascii'}
        """
        if method == 'unicode':
            return ''.join(
                c
                for c in unicodedata.normalize('NFKD', text)
                if not unicodedata.combining(c)
            )
        elif method == 'ascii':
            return (
                unicodedata.normalize('NFKD', text)
                .encode('ascii', errors='ignore')
                .decode('ascii')
            )
        else:
            msg = '`method` must be either "unicode" and "ascii", not {}'.format(method)
            raise ValueError(msg)

    def scrub(self, text, unicode_normalization='NFC', accent_removal_method='unicode'):
        """Normalize whitespace and and bad unicode, and remove accents.

        Parameters:
        - unicode_normalization: The ftfy.fix_text() `normalization` parameter.
        - accent_removal_method: The Doc.remove_accents() `method` parameter.

        """
        # Change multiple spaces to one and multiple line breaks to one.
        # Also strip leading/trailing whitespace.
        text = NONBREAKING_SPACE_REGEX.sub(' ', LINEBREAK_REGEX.sub(r'\n', text)).strip()
        # Combine characters and diacritics written using separate code points
        text = fix_text(text, normalization=unicode_normalization)
        text = self._remove_accents(text, method=accent_removal_method)
        return text

    def _read_manifest(self):
        """Read a JSON file and return a Python dict."""
        with open(self.manifest_filepath, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
        
    def _get_docstring(self, content_property):
        """Extract a document string from a manifest property."""
        return self.manifest_dict[content_property]

    def get_features(self):
        """Process the document with the spaCy pipeline into a pandas dataframe.
        
        If `collect_readability_scores` is set, Flesch-Kincaid Readability,
        Flesch-Kincaid Reading Ease and Dale-Chall formula scores are collected
        in a tuple in that order. Other formulas are available (see 
        https://github.com/mholtzscher/spacy_readability).
        
        Parameters:
        - as_list: Return the features as a list instead of a dataframe.

        """
        # Handle optional pipes
        if 'merge_noun_chunks' in self.options and self.options['merge_noun_chunks'] == True:
            merge_nps = self.nlp.create_pipe('merge_noun_chunks')
            self.nlp.add_pipe(merge_nps)
        if 'merge_subtokens' in self.options and self.options['merge_subtokens'] == True:
            merge_subtok = self.nlp.create_pipe('merge_subtokens')
            self.nlp.add_pipe(merge_subtok)
        # Build the feature list
        feature_list = []
        columns = ['TOKEN', 'NORM', 'LEMMA', 'POS', 'TAG', 'STOPWORD', 'ENTITIES']
        for token in self.content:
            # Get named entity info (I=Inside, O=Outside, B=Begin)
            ner = (token.ent_iob_, token.ent_type_)
            t = [token.text, token.norm_, token.lemma_, token.pos_, token.tag_, str(token.is_stop), ner]
            feature_list.append(tuple(t))
        return pd.DataFrame(feature_list, columns=columns)

    def filter(self, pattern=None, column='TOKEN', skip_punct=False, skip_stopwords=False, skip_linebreaks=False, case=True, flags=0, na=False, regex=True):
        """Return a new dataframe with filtered rows.

        Parameters:
        - pattern: The string or regex pattern on which to filter.
        - column: The column where the string is to be searched.
        - skip_punct: Do not include punctuation marks.
        - skip_stopwords: Do not include stopwords.
        - skip_linebreaks: Do not include linebreaks.
        - case: Perform a case-sensitive match.
        - flags: Regex flags.
        - na: Filler for empty cells.
        - regex: Set to True; otherwise absolute values will be matched.
        The last four parameters are from `pandas.Series.str.contains`.

        """
        # Filter based on column content
        new_df = self.features
        if pattern is not None:
            new_df = new_df[new_df[column].str.contains(pattern, case=case, flags=flags, na=na, regex=regex)]
        # Filter based on token type
        if skip_punct == True:
            new_df = new_df[~new_df['POS'].str.contains('PUNCT', case=True, flags=0, na=False, regex=True)]
        if skip_stopwords == True:
            new_df = new_df[~new_df['STOPWORD'].str.contains('TRUE', case=False, flags=0, na=False, regex=True)]
        if skip_linebreaks == True:
            new_df = new_df[~new_df['POS'].str.contains('SPACE', case=True, flags=0, na=False, regex=True)]
        return new_df

    def lemmas(self, as_list=False):
        """Return a dataframe containing just the lemmas."""
        if as_list == True:
            return [token.lemma_ for token in self.content]
        else:
            return pd.DataFrame([token.lemma_ for token in self.content], columns=['LEMMA'])

    def punctuation(self, as_list=False):
        """Return a dataframe containing just the punctuation marks."""
        if as_list == True:
            return [token.text for token in self.content if token.is_punct]
        else:
            return pd.DataFrame([token.text for token in self.content if token.is_punct], columns=['PUNCTUATION'])

    def pos(self, as_list=False):
        """Return a dataframe containing just the parts of speech."""
        if as_list == True:
            return [token.pos_ for token in self.content]
        else:
            return pd.DataFrame([token.pos_ for token in self.content], columns=['POS'])

    def tags(self, as_list=False):
        """Return a dataframe containing just the tags."""
        if as_list == True:
            return [token.tag_ for token in self.content]
        else:
            return pd.DataFrame([token.tag_ for token in self.content], columns=['TAG'])

    def entities(self, options=['text', 'label'], as_list=False):
        """Return a dataframe containing just the entities from the document.
        
        Parameters:
        - options: a list of attributes ('text', 'start', 'end', 'label')
        - as_list: return the entities as a list of tuples.

        """
        ents = []
        for ent in self.content.ents:
            e = []
            if 'text' in options:
                e.append(ent.text)
            if 'start' in options:
                e.append(ent.start)
            if 'end' in options:
                e.append(ent.end)
            if 'label' in options:
                e.append(ent.label_)
            ents.append(tuple(e))
        if as_list == True:
            return ents
        else:
            return pd.DataFrame(ents, columns=[option.title() for option in options])

    def readability_scores(self, columns=['Flesch-Kincaid Readability',
        'Flesch-Kincaid Reading Ease', 'Dale-Chall'], as_list=False):
        """Get a list of readability scores from the document.
        
        Parameters:
        - columns: a list of labels for the score types
        - as_df: return the list as a dataframe.

        """
        fkr = self.content._.flesch_kincaid_reading_ease
        fkg = self.content._.flesch_kincaid_grade_level
        dc = self.content._.dale_chall
        scores = [(fkr, fkg, dc)]
        if as_list == True:
            return scores
        else:
            return pd.DataFrame(scores, columns=columns)

    def stems(self, stemmer='porter', as_list=False):
        """Convert the tokens in a spaCy document to stems.

        Parameters:
        - stemmer: the stemming algorithm ('porter' or 'snowball').
        - as_list: return the dataframe as a list.

        """
        if stemmer == 'snowball':
            stemmer = SnowballStemmer(language='english')
        else:
            stemmer = PorterStemmer()
        stems = [stemmer.stem(token.text) for token in self.content]
        if as_list == True:
            return stems
        else:
            return pd.DataFrame(stems, columns=['Stems'])

    def ngrams(self, n=2, as_list=False):
        """Convert the tokens in a spaCy document to ngrams.

        Parameters:
        - n: The number of tokens in an ngram.
        - as_list: return the dataframe as a list.

        """
        ngram_tokens = list(ngrams([token.text for token in self.content], n))
        if as_list == True:
            return ngram_tokens
        else:
            prefix = str(n) + '-'
            if n == 2:
                prefix = 'Bi'
            if n == 3:
                prefix = 'Tri'
            label = prefix + 'grams'
            return pd.DataFrame({label: pd.Series(ngram_tokens)})

    def remove_property(self, properties, save=False):
        """Remove a property from the manifest.

        Parameters:
        - property: The property or a list of properties to be removed from the manifest.
        - save: Save the deletion to the manifest.

        """
        for property in properties:
            del self.manifest_dict[property]
        # Write the json to the manifest file
        # IMPORTANT: May not work if the manifest file has binary content
        with open(self.manifest_filepath, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.manifest_dict))
            
    def serialize(self, df, indent=None):
        """Serialize a dataframe as a list of lists with the column headers as the first element.

        Parameters:
        - indent: An integer indicating the number of spaces to indent the json string. Default is None.

        """
        j = json.loads(pd.DataFrame.to_json(df, orient='values'))
        j.insert(0, list(df.columns))
        return json.dumps(j, indent=indent)

    def deserialize(self, j):
        """Deserialize a list of lists to a dataframe using the first element as the headers."""
        df = pd.read_json(j, orient='values')
        headers = df.iloc[0]
        return pd.DataFrame(df.values[1:], columns=headers)


    def save(self, property=None, series=None, sort=False):
        """Convert a series of values and save them to the manifest file.
        
        Overwrites the original manifest file, so not to be used lightly.
        IMPORTANT: May not work if the manifest file has binary content.
        Parameters:
        - property: A string naming the JSON property to save to.
        - series: The list or dataframe to save.
        - sort: Alphabetically sort the series to lose token order.

        """
        with open(self.manifest_filepath, 'w', encoding='utf-8') as f:
            if isinstance(series, dict) or isinstance(series, list):
                self.manifest_dict[property] = series
                f.write(json.dumps(self.manifest_dict))
            else:
                if sort == True:
                    col = list(series.columns)[0]
                    series.sort_values(by=[col], inplace=True)
                json_str = self.serialize(series)
                self.manifest_dict[property] = json.loads(json_str)
                f.write(json_str)

class Preprocessor:
    """Configure a preprocessor object."""

    def __init__(self, model='en_core_web_sm', sources_csv=None):
        """Initialize the preprocessor."""

        # Load the language model
        print('Preparing language model...')
        self.nlp = spacy.load(model)

        # Import readability
        print('Testing readability...')
        try:
            from spacy_readability import Readability
            self.collect_readability_scores = True
        except:
            msg = """The spacy-readability module is not installed on your system.
            Readability scores will be unavailable unless you `pip install spacy-_readability`."""
            print(msg)
            self.collect_readability_scores = False
            pass
        
        # Configure language model options
        self.add_stopwords = []
        self.remove_stopwords = []
        self.skip_entities = ['CARDINAL', 'DATE (except months)', 'QUANTITY', 'TIME']
        self.lemmatization_cases = {
            "humanities": [{ORTH: u'humanities', LEMMA: u'humanities', POS: u'NOUN', TAG: u'NNS'}]
        }
    
        # Configure entity categories to be skipped when merging entities
        self.options = {
            'merge_noun_chunks': False,
            'merge_subtokens': False,
            'skip_ents': self.skip_entities,
            'collect_readability_scores': self.collect_readability_scores
            }
    
        # Handle lemmatisation exceptions
        for k, v in self.lemmatization_cases.items():
            self.nlp.tokenizer.add_special_case(k, v)
        
        # Add and remove custom stop words
        for word in self.add_stopwords:
            self.nlp.vocab[word].is_stop = True
        for word in self.remove_stopwords:
            self.nlp.vocab[word].is_stop = False
        
        self.nlp.add_pipe(self.skip_ents, after='ner')
        
        # Add readability to pipeline
        if self.collect_readability_scores == True:
            self.nlp.add_pipe(Readability())
        
        # Load the sources file
        self.sources = ''
        if sources_csv:
            with open(sources_csv, 'r') as f:
                self.sources = [dict(line) for line in csv.DictReader(f)]

    # Add Custom Tokenizer if needed
    def custom_tokenizer(self, nlp):
        """Add custom tokenizer settings."""
        # nlp.tokenizer = custom_tokenizer(nlp)
        return Tokenizer(nlp.vocab, prefix_search=PREFIX_RE.search,
                                    suffix_search=SUFFIX_RE.search,
                                    infix_finditer=INFIX_RE.finditer,
                                    token_match=SIMPLE_URL_RE.match)

    # Custom entity merging filter
    def skip_ents(self, doc, skip=['CARDINAL', 'DATE', 'QUANTITY', 'TIME']):
        """Duplicate spaCy's ner pipe, but with additional filters.

        Parameters:
        - doc (Doc): The Doc object.
        - ignore (list): A list of spaCy ner categories to ignore (e.g. DATE) when merging entities.
        
        RETURNS (Doc): The Doc object with merged entities.

        """
        # Match months
        months = re.compile(r'(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|Dec(?:ember)?)')
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                merge = True
                if ent.label_ in skip:
                    merge = False
                if ent.label_ == 'DATE' and re.match(months, ent.text.lower()):
                    merge = True
                if merge == True:
                    attrs = {"tag": ent.root.tag, "dep": ent.root.dep, "ent_type": ent.label}
                    retokenizer.merge(ent, attrs=attrs)
        return doc

    # Not part of the Document class for ease of access.
    # Create bags as separate dicts and then save them to the manifest.
    def bagify(self, series, trim_punct=True, as_counter=False):
        """Convert a list of values to a dict of value frequencies.
        
        Parameters:
        - trim_punct: If True, strips attached punctuation that may have survived tokenisation.
        - as_counter: If True, returns a Python Counter object enabling its most_common() method.

        """
        # An attempt to strip predictably meaningless stray punctuation
        punct = re.compile(r'\.\W|\W\.|^[\!\?\(\),;:\[\]\{\}]|[\!\?\(\),;:\[\]\{\}]$')
        # Make sure we are working with a list of values
        if isinstance(series, pd.DataFrame):
            print('Please select only one columns from the dataframe.')
        if isinstance(series, pd.Series):
            if trim_punct == True:
                series = [re.sub(punct, '', term) for term in list(series.values)]
            else:
                series = [term for term in list(series.values)]
        if as_counter == True:
            return Counter(series)
        else:
            return dict(Counter(series))

    def preprocess_dir(self, manifest_dir, content_property, kwargs=None):
        """Walk through a directory of folders and preprocess the json files.
        
        Parameters:
        - content_property: The manifest property to be used as the source of the content.
        - add_properties: A list of properties to add to the manifest. Default is `None`.
          If the property includes options the values should be separated by colons (e.g.
          `ngrams:2` for bigrams or `stems:snowball` for the Snowball stemmer.)
        - remove_properties: A list of properties to remove from the manifest. Default is `None`.
        - kwargs: A dict of options to pass to the main preprocessing function.

        """
        # Start the timer
        start = time.time()
        # Walk the directory and preprocess each file
        all_files = [os.path.join(r, file) for r, d, f in os.walk(manifest_dir) for file in f]
        for file in all_files:
            if file.endswith('.json') and not file.startswith('._'):
                file = file.replace('\\', '/') # Handle Windows paths
                tmp = file.split('/')
                path = '/'.join(tmp[:-1])
                filename = tmp[-1]
                self.preprocess(path, filename, content_property, kwargs=None)
        # Print time to completion
        end = time.time()
        t = end - start
        print('Processed all files in ' + str(t) + ' seconds.')
    
    def preprocess_file(self, manifest_dir, filename, content_property, kwargs=None):
        """Preprocess a specific json file.
        
        Parameters:
        - content_property: The manifest property to be used as the source of the content.
        - add_properties: A list of properties to add to the manifest. Default is `None`.
          If the property includes options the values should be separated by colons (e.g.
          `ngrams:2` for bigrams or `stems:snowball` for the Snowball stemmer.)
        - remove_properties: A list of properties to remove from the manifest. Default is `None`.
        - kwargs: A dict of options to pass to the main preprocessing function.

        """
        self.preprocess(manifest_dir, filename, content_property, kwargs)
    
    def preprocess(self, manifest_dir, filename, content_property, kwargs=None, add_properties=None, remove_properties=None):
        """Start the main preprocessing function."""
        # Start doc timer
        doc_start = time.time()
    
        # Initialise the Document object
        try: 
            doc = Document(manifest_dir, filename, content_property=content_property, model=self.nlp, kwargs=kwargs)
        except UnicodeDecodeError as error:
            print('Document failed:', filename)
            print(error)
            return False
    
        # # Make sure the specified json property containing content exits
        # if content_property not in doc.manifest_dict:
        #     if 'content_unscrubbed' in doc.manifest_dict:
        #         doc = Document(manifest_dir, filename, content_property='content_unscrubbed', model=self.nlp, kwargs=kwargs)
        #     else:
        #         doc = Document(manifest_dir, filename, content_property='content', model=self.nlp, kwargs=kwargs)
    
        # Remove manifest properties if the remove_properties list is submitted
        if remove_properties is not None:
            doc.remove_property(remove_properties, save=False)
    
        # Sort and serialise the features table
        features = doc.get_features()
        features.sort_values(by=['TOKEN'], inplace=True)
        features_list = json.loads(pd.DataFrame.to_json(features, orient='values'))
        features_list.insert(0, list(features.columns))
        doc.manifest_dict['features'] = features_list
    
        # Bagify the normed tokens (skipping punctuation and line breaks)
        # Attempt to remove stray punctuation
        punct = re.compile(r'\.\W|\W\.|^[\!\?\(\),;:\[\]\{\}]|[\!\?\(\),;:\[\]\{\}]$')
        filtered = [re.sub(punct, '', token.norm_) for token in doc.content if token.norm_ != '_' and token.is_punct != True and token.is_space != True and token.is_digit !=True]
        filtered = sorted(filtered)
        doc.manifest_dict['bag_of_words'] = dict(Counter(filtered))
    
        # Add any additional properties to the manifest:
        if add_properties is not None:
            for property in add_properties:
                if property == 'lemmas':
                    doc.manifest_dict['lemmas'] = doc.lemmas(as_list=True)                
                if property == 'punctuation':
                    doc.manifest_dict['punctuation'] = doc.punctuation(as_list=True)
                if property == 'pos':
                    doc.manifest_dict['pos'] = doc.pos(as_list=True)
                if property == 'tags':
                    doc.manifest_dict['tags'] = doc.tags(as_list=True)
                if property.startswith('stems'):
                    options = property.split(':')
                    doc.manifest_dict['stems'] = doc.stems(stemmer=options[1], as_list=True)
                if property.startswith('ngrams'):
                    doc.manifest_dict['ngrams'] = doc.ngrams(n=options[1], as_list=True)
        
        # Add the readability scores to the manifest
        doc.manifest_dict['readability_scores'] = doc.readability_scores(as_list=True)[0]
        
        # Add the total word count (skipping punctuation and line breaks) to the manifest
        doc.manifest_dict['word_count'] = len(doc.filter(column='TOKEN', skip_punct=True, skip_stopwords=False, skip_linebreaks=True))
    
        # Add the country in which the document was published
        if self.sources:
            doc.manifest_dict['country'] = [x for x in self.sources if x['source_title'] == doc.manifest_dict['pub']][0]['country']
    
        # Add language model metadata
        doc.manifest_dict['language_model'] = self.nlp.meta
        custom = {
            'linebreak_regex': str(LINEBREAK_REGEX),
            'nonbreak_regex': str(NONBREAKING_SPACE_REGEX),
            'prefix_re': str(PREFIX_RE),
            'suffix_re': str(SUFFIX_RE),
            'infix_re': str(INFIX_RE),
            'simple_url_re': str(SIMPLE_URL_RE),
            'add_stopwords': self.add_stopwords,
            'remove_stopwords': self.remove_stopwords,
            'lemmatization_cases': self.lemmatization_cases,
            'skip_entities': self.skip_entities
        }
        doc.manifest_dict['language_model']['custom'] = custom
    
        # Save the changes to the manifest
        with open(doc.manifest_filepath, 'w', encoding='utf-8') as f:
            f.write(json.dumps(doc.manifest_dict))
        
        # Print time to completion
        doc_end = time.time()
        doc_t = doc_end - doc_start
        print('Processed ' + doc.manifest_filepath + ' in ' + str(doc_t) + ' seconds.')


# def main(**kwargs):
#     """Capture the command line arguments and fire the preprocessor."""
#     pp = Preprocessor()
#
#     add_properties = None
#     remove_properties = None
#     # Because we don't want to pass a long dict on the command line, we set options here.
#     options = {'merge_noun_chunks': False, 'merge_subtokens': False, 'collect_readability_scores': pp.collect_readability_scores}
#     try:
#         manifest_dir = kwargs['path']
#     except:
#         raise KeyError('Please supply a directory path with `--path`.')
#     if 'filename' in kwargs:
#         manifest_file = kwargs['filename']
#     else:
#         manifest_file = None
#     try:
#         content_property = kwargs['property']
#     except:
#         raise KeyError("Please supply a JSON property where the document's content is found with `--property`.")
#     if 'add_properties' in kwargs and kwargs['add_properties'] is not None:
#         try:
#             if isinstance(kwargs['add_properties'], tuple):
#                 add_properties = list(kwargs['add_properties'])
#             else:
#                 add_properties = [kwargs['add_properties']]
#             if len(add_properties) == 0:
#                 add_properties = None
#         except:
#             raise ValueError('The `add-properties` parameter must contain multiple values separated by commas.')
#     if 'remove_properties' in kwargs and kwargs['remove_properties'] is not None:
#         try:
#             if isinstance(kwargs['remove_properties'], tuple):
#                 remove_properties = list(kwargs['remove_properties'])
#             else:
#                 remove_properties = [kwargs['remove_properties']]
#             if len(remove_properties) == 0:
#                 remove_properties = None
#         except:
#             raise ValueError('The `remove-properties` parameter must contain multiple values separated by commas.')
#
#     if manifest_file is not None:
#         print('Starting preprocessing...')
#         pp.preprocess_file(manifest_dir, manifest_file, content_property, kwargs=options)
#         print('Finished preprocessing file.')
#     else:
#         print('Starting preprocessing...')
#         pp.preprocess_dir(manifest_dir, content_property, kwargs=options)
#         print('Finished preprocessing directory.')
#
#
# if __name__ == '__main__':
#   fire.Fire(main)

