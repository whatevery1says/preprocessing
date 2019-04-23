import spacy

# NB. This model is too small for practical use.
# Switch to 'en_core_web_lg'
nlp = spacy.load('en_core_web_sm')

def get_pos(content, merge_noun_phrases=False, merge_subtokens=False)
    """Return a list of POS tokens.

    Options are to merge noun phrases and to merge token which 
    Spacy predicts should be merged.
    """
    content = nlp(content)
    if merge_noun_phrases:
        merge_nps = nlp.create_pipe("merge_noun_chunks")
        nlp.add_pipe(merge_nps)
    if merge_noun_phrases:
        merge_subtok = nlp.create_pipe("merge_subtokens")
        nlp.add_pipe(merge_subtok)
    pos_tokens = []
    for token in content:
        pos_tokens.append(token)
    return pos_tokens

def lemmatize(content):
    """Return a list of lemmas in the document."""
    return [w.lemma_ for w in nlp(content)]

def ner(content, merge_entities=True):
    """Return a list of named entities.

    There is an option to merge entity tokens like "New York" and "David Bowie".
    """
    content = nlp(content, disable=['parser'])
    if merge_entities:
        merge_ents = nlp.create_pipe("merge_entities")
        nlp.add_pipe(merge_ents)
    return content.ents

# Add extra features to the manifest for every document in a corpus
for doc in corpus:
    doc['pos_tokens'] = get_pos(doc['content'])
    doc['lemmas'] = lemmatize(doc['content'])
    doc['entities'] = ner(doc['content'], merge_entities=True)