# The `preprocess.py` script

The `preprocess.py` script is available at [https://github.com/whatevery1says/preprocessing/blob/master/preprocess.py](https://github.com/whatevery1says/preprocessing/blob/master/preprocess.py).

This script is only for preprocessing from the command line. It performs the following algorithm:

1. Reads the JSON manifest(s) into a spaCy nlp object.
2. Removes properties from the manifest, if specified.
3. Generates a table of spaCy nlp features, sorts it, and adds it without indexes to the manifest. The structure is a list of lists.
4. Creates a bag of terms dict (not including punctuation and line breaks) and adds it to the manifest.
5. Adds any additional specified properties (e.g. stems or ngrams) as lists to the manifest.
6. Adds a list of the document's readability scores to the manifest.
7. Adds the total word count (skipping punctuation and line breaks) to the manifest.    
8. Saves the new manifest over the old one.
    
This entire process took between 3-4 seconds for 11 files on my laptop.

The command line arguments are as follows:

- `--path` (required): The file path to the directory containing the JSON manifest file. The script should walk through subdirectories.
- `--filename` (required): The name of the JSON manifest file .json with extension.
- `--property` (required): The name of the JSON property to be preprocessed.
- `--add-properties` (optional): A comma-separated list of properties to be added to the manifest file.
- `--remove-properties` (optional): A comma-separated list of properties to be removed from the manifest file.  

## Preprocessing a single file

**Sample commands**

```
python preprocess.py --path=data --filename=2010_10_humanities_student_major_5_askreddit.json --property=content_scrubbed

python preprocess.py --path=data --filename=2010_10_humanities_student_major_5_askreddit.json --property=content --remove-properties=content_scrubbed
```

## Preprocessing a directory of files

**Sample commands**

```
python preprocess.py --path=data --property=content_scrubbed

python preprocess.py --path=data --property=content --remove-properties=content_scrubbed
```

## To Do

- Some fine tuning may be needed for the language model.
- WE1S windowed ngrams need to be added. Right now only normal ngrams work.
