# preprocessing

Test repo for WE1S preprocessing script.

## Preliminary Description of the WE1S Preprocessing Pipeline

1. Normalise whitespace and bad unicode

  a. Match `r'((\r\n)|[\n\v])+'` and replace it with `'\n'`  
  b. Match `r'(?!\n)\s+')` and replace it with `' '`  
  c. Trim whitespace from at the start and end of the string
  d. Normalise the Unicode according 'NFKD' method  
  e. If an accented character is Unicode, replace it with an unaccented ASCII equivalent by normalising it according 'NFKD' method.

2. Tokenise according to spaCy's pipeline (see below) using the following settings:

```python
PREFIX_RE = re.compile(r'''^[\[\]\("'\.,;:-]''')
SUFFIX_RE = re.compile(r'''[\[\]\)"'\.,;:-]$''')
INFIX_RE = re.compile(r'''[-~]''')
SIMPLE_URL_RE = re.compile(r'''^https?://''')
```

3. When parsing the word "humanities", do not lemmatise it as "humanity".

4. Re-tokenise the text merging entities into tokens using spaCy's named entity recognition. Do not tag cardinal numbers, dates (except months), quantities, or times as entities.

5. Remove stop words from the WE1S standard list.

6. From the remaining tokens, try to remove meaningless punctuation using the regex pattern `r'\.\W|\W\.|^[\!\?\(\),;:\[\]\{\}]|[\!\?\(\),;:\[\]\{\}]$'`.

7. Create a term count matrix.

8. Generate a "vectors" file where each document is on a separate line and terms appearing N times in the document are repeated N times. All terms are separated by spaces.

9. Import into MALLET using `--token-regex "\S+"`. Do not strip stopwords.

Note that Twitter is preprocessed according to a variant of this pipeline for which the documentation is pending.

## The spaCy Pipeline

The main WE1S corpus has linguistic features extracted using spaCy's [en_core_web_lg](https://spacy.io/models/en#en_core_web_lg) language model. The preprocessor records a `features` table containing a row for each token, normalised (lower-cased) token, lemma, part of speech, detailed part of speech (tag), and named entity. The `features` table is saved to the document's manifest and is accessible for extracting features from the document without repeated parsing. However, because the original text may be reconstructed from the features table, which preserves token order, public document manifests may have the table sorted.

Detailed information about spaCy's linguistic feature extraction can be found on the [spaCy website](https://spacy.io/usage/linguistic-features). Some features extracted during preprocessing are not preserved in the documents `features` table.

### Tokenisation

spaCy tokenizes documents by applying rules from its language model to segment the text into words, punctuation and so on. Whitespace information is preserved in the tokens and no information is added or removed. As a result, the `features` table contains punctuation and line breaks, which are treated as tokens.

After the tokens are split on spaces (`' '`), spaCy then perform two checks on the resulting substrings:

1. Does the substring match an exception rule

First, the raw text is split on whitespace characters, similar to text.split(' '). Then, the tokenizer processes the text from left to right. On each substring, it performs two checks:

- Does the substring match one of the language model's tokenizer exception rules, such as splitting “don’t” but leaving “U.K.” as one?
- Does the substring contain a prefix, suffix or infix (typically punctuation marks, hyphens, or quotes) that can be split off?

If so, these rules are applied before the spaCy continues to the next substring. Note that WE1S uses customised prefix, suffix, and infix patterns listed above.

## Lemmatisation and Part of Speech Tagging

spaCy uses rules in its language model to identify lemmas and parts of speech for each token. Although spaCy is very accurate, the accuracy does vary with the type of data. By default, it lemmatises "humanities" as "humanity", so the WE1S pipeline applies an exception to this rule.

## Named Entity Recognition

Named entity recognition is applied after tokenisation, lemmatisation, and part of speech tagging. spaCy uses rules in its language model to identify named entities. As with lemmatisation and parts of speech, accuracy depends on the data. Named entities are tagged with a wide variety of descriptive labels, which are described [here](https://spacy.io/api/annotation#named-entities).

spaCy typically identifies space-separated phrases (e.g. "Toni Morrison") as named entities. Phrases like these have to be converted to "toni_morrison" for use in WE1S visualisations, and the result of spaCy named entity recognition is a proliferation of underscored phrases. In order to avoid this, the WE1S pipeline customises spaCy's named entity recognition by skipping some categories of entities. These include the categories CARDINAL, DATE (but dates containing the names of months are allowed), QUANTITY, and TIME.
