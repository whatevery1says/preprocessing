# README for `vectors.py`

`vectors.py` creates a `Vectors` object that handles the creation of vectors files to be imported by MALLET. Although a `Vectors` object can be created on a document with `vectors=Vectors(0, 'manifest_path.json', 'vectors_path.txt', model='en_core_web_sm', stoplist='we1s_standard_stoplist.txt')`, it will typically used with a directory of json files by means of the `vectorize_dir()` function. Here is a sample usage:

```python
vectorize_dir('caches/json',
              'model/vectors.txt',
              'en_core_web_lg',
              stoplist='libs/vectors/we1s_standard_stoplist.txt'
              )
```

This function loops through a sorted list of json files in the directory, creates a `Vectors` object from each one, and saves its vectors as a row in the `vectors.txt` file. This is the file that will be imported by MALLET.

If stop words are to be filtered prior to topic modelling, `vectorize_dir()` should be fed a stoplist file. If none is provided, the stoplist file at the file path shown above (unless this is changed in production). If you do not want to strip stop words, give it an empty file. See the section on stop words below.

The `Vectors` class assumes that the document's manifest will have a `bag_of_words` field, which it will use to extract the vectors. If no `bag_of_words` field exists, it will attempt to use the token list from the `features` field. If that does not exist, it will tokenise the contents of the `content` field and use that to create a bag of words.

The `Vectors` object will have a `vectors` property, which is a row of key-value pairs showing the document's term counts (preceded by a document index number and the name of the json file). `vectorize_dir()` automatically calls `Vectors.save()`, which appends the row to the `vectors.txt` file. When the process is complete, the file is ready to be imported to MALLET.

## Stop Words

This section documents the logic behind our use of stop words and the provenance of our stop list (currently named `we1s_standard_stoplist.txt`). Eventually, this section should probably be moved to a more prominent location.

The standard WE1S workflow has the following steps:

1. Tokenise the document with spaCy. This step tags each token with a Boolean `is_stop` to indicate whether or not the word occurs in spaCy's static stoplist. All documents are pre-processed with this step.
2. At the project level, all document tokens, including spaCy's stop words, are processed into bags of words, which are then by default filtered using `we1s_standard_stoplist.txt` _before_ these bags are imported by MALLET.
3. MALLET's own tokenisation and stop word removal functions are disabled.

This procedure ensures consistent tokenisation and stop words across the entire workflow.

The WE1S Standard Stoplist is at this stage provisional. It aims to strike a balance between spaCy's smaller stop list and MALLET's more extensive one. spaCy's stop list is an extension Stone, Denis, and Kwantes (2010), with some extra handling of English contractions. MALLET's stop list appears to be derived from the [SMART Information Retrieval System](https://en.wikipedia.org/wiki/SMART_Information_Retrieval_System). See Igor Brigadir, [Default English stopword lists from many different sources](https://github.com/igorbrigadir/stopwords) and Yothman, Qin, and Yurchak, [Stop Word Lists in Free Open-source Software Packages](https://aclweb.org/anthology/W18-2502) (2018) for further discussion of the provenance of these stop lists.

The WE1S Standard Stoplist was formed by combining spaCy's 339 stop words with MALLET's 524. A few words of potential relevance to discussion about the humanities like "old", "new", and "novel" were removed, along with some likely meaningful but low frequency terms. This process was necessarily subjective, the likely consequences of which are discussed below. The resulting stoplist contains 497 terms. This includes a number of particles from the MALLET list like "ve" (from "I've"). We expect the WE1S customisation of spaCy's tokeniser to prevent such tokens from getting to the bag of words stage, but we have kept the particles in the stoplist as fail safes.

Although the choice to include or exclude potentially meaningful terms is a subjective one, we note that in [Schofield, Magnusson, Mimno, "Pulling Out the Stops: Rethinking Stopword Removal for Topic Models" (2017)](http://www.cs.cornell.edu/~xanda/stopwords2017.pdf) find that such choices are unlikely to affect the resulting topic models, and that the legibility of these models can be better improved by postprocessing. Combining the spaCy and MALLET lists goes some way towards addressing the suggestion by Yothman, Qin, and Yurchak that stoplists apply a more complete and consistent set of inflected forms for verbs. The WE1S could perhaps still be improved by applying this principle more systematically.
