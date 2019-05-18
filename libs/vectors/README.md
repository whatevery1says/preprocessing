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

If stop words are to be filtered prior to topic modelling, `vectorize_dir()` should be fed a stoplist file. If none is provided, the stoplist file at the file path shown above (unless this is changed in production). If you do not want to strip stop words, give it an empty file.

The `Vectors` class assumes that the document's manifest will have a `bag_of_words` field, which it will use to extract the vectors. If no `bag_of_words` field exists, it will attempt to use the token list from the `features` field. If that does not exist, it will tokenise the contents of the `content` field and use that to create a bag of words.

The `Vectors` object will have a `vectors` property, which is a row of key-value pairs showing the document's term counts (preceded by a document index number and the name of the json file). `vectorize_dir()` automatically calls `Vectors.save()`, which appends the row to the `vectors.txt` file. When the process is complete, the file is ready to be imported to MALLET.
