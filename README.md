# preprocessing

Test repo for WE1S preprocessing script.

## Preliminary Description of the WE1S Preprocessing Pipeline

1. Normalise whitespace and bad unicode

  a. Match `r'((\r\n)|[\n\v])+'` and replace it with `'\n'`
  b. Match `r'(?!\n)\s+')` and replace it with `' '`
  c. Trim whitespace from at the start and end of the string
  d. Normalise the Unicode according 'NFKD' method
  e. If an accented character is Unicode, replace it with an unaccented ASCII equivalent by normalising it according 'NFKD' method.

2. Tokenise according to spaCy's pipeline using the following settings:

```python
PREFIX_RE = re.compile(r'''^[\[\]\("'\.,;:-]''')
SUFFIX_RE = re.compile(r'''[\[\]\)"'\.,;:-]$''')
INFIX_RE = re.compile(r'''[-~]''')
SIMPLE_URL_RE = re.compile(r'''^https?://''')
```

3. When parsing the word "humanities", do not lemmatise it as "humanity".

4. Re-tokenise the text merging entities into tokens using spaCy's named entity recognition. Do not tag cardinal numbers dates (except months), quantities, or times as entities.

5. Remove stop words from the WE1S standard list.

6. From the remaining tokens, try to remove meaningless punctuation using the regex pattern `r'\.\W|\W\.|^[\!\?\(\),;:\[\]\{\}]|[\!\?\(\),;:\[\]\{\}]$'`.

7. Create a term count matrix.

8. Generate a "vectors" file where each document is on a separate line and terms appearing N times in the document are repeated N times. All terms are separated by spaces.

9. Import into MALLET using `--token-regex "\S+"`. Do not strip stopwords.

Note that Twitter is preprocessed according to a variant of this pipeline for which the documentation is pending.
