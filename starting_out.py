import json
import os
import pandas as pd
import spacy

# Configuration
data_dir = 'data'
filename = os.listdir(data_dir)[0] # The first file in the corpus

# NB. This model is too small for practical use.
# Switch to 'en_core_web_lg' for production
nlp = spacy.load('en_core_web_sm')

def ner(content, merge_entities=True):
    """Return a list of named entities.

    There is an option to merge entity tokens like 
    'New York' and 'David Bowie'.
    """
    content = nlp(content, disable=['parser'])
    if merge_entities:
        merge_ents = nlp.create_pipe('merge_entities')
        nlp.add_pipe(merge_ents)
    return content.ents

def get_features(content, merge_noun_phrases=False, merge_subtokens=False):
    """Return a list of doc tokens.

    Options are to merge noun phrases and to merge tokens which 
    Spacy predicts should be merged.
    """
    content = nlp(content)
    if merge_noun_phrases:
        merge_nps = nlp.create_pipe('merge_noun_chunks')
        nlp.add_pipe(merge_nps)
    if merge_noun_phrases:
        merge_subtok = nlp.create_pipe('merge_subtokens')
        nlp.add_pipe(merge_subtok)
    features = []
    for token in content:
        features.append((token.text, token.lemma_, token.pos_, token.tag_))
    return features

def read_file(data_dir, filename):
    """Read a JSON file as a Python dict."""
    with open(os.path.join(data_dir, filename), 'r') as f:
        return json.loads(f.read())

def features_to_df(features):
    """Convert a JSON list of features to a Pandas dataframe."""
    return pd.DataFrame(features, columns=['Text', 'Lemma', 'POS', 'Tag'])

def features_from_json(features):
    """Convert a Pandas dataframe of features to a JSON list."""
    df = pd.read_json(features, orient='values')
    df.columns=['Text', 'Lemma', 'POS', 'Tag']
    return df

def save_features(data_dir, filename, features):
    """Save a generated JSON list of features to a JSON manifest."""
    with open(os.path.join(data_dir, filename), 'r') as f:
        doc = json.loads(f.read())
        doc['features'] = features
    with open(os.path.join(data_dir, filename), 'w') as f:
        f.write(json.dumps(doc))

def generate_features(data_dir, filename, display=False, save=False):
    """ Generate and save document features to the manifest."""
    # Read the manifest file
    doc = read_file(data_dir, filename)
    # Get the features
    features = get_features(doc['content_scrubbed'])
    # Convert the feature tuples to a dataframe
    df = features_to_df(features)
    # Convert the dataframe to a JSON string
    doc['features'] = df.to_json(orient='values')
    if display == True:
        print(doc['features'])
    if save == True:
        save_features(data_dir, filename, doc['features'])

def doc_features(data_dir, filename):
    """Return a dataframe containing the manifest features."""
    # Read the manifest and convert features to a dataframe
    return features_from_json(read_file(data_dir, filename)['features'])

# Generate and save the features for a file
generate_features(data_dir, filename, display=False, save=True)

# Get the features for a file
doc_features = doc_features(data_dir, filename)
print(doc_features)

