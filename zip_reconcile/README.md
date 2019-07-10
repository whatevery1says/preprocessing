# 2019-07-10 towards renaming script for zips baremetal to harbor

They were renamed on harbor manually, if we ever reprocess again we need to do it again -- make a script mapping to new names.

Also, current renaming leaves out-of-date JSON names inside the renamed zip files -- make the script rename the JSONs, eg using ZipEditor.


## NOTES

-merged files are the two baremetal folder files, combined (respectively)
harbor- files are those files with Lindsay's rename labor on harbor

zip renaming for 
	opendiff humanities-merged-edit.txt harbor-humanities-keywords.txt 
	opendiff comparison-merged.txt harbor-comparison-corpus.txt 
	
comparison renaming:

	6742_newyorktimes -> 6742_thenewyorktimes
	8006_losangelestimes -> 8006_thelatimes
	8075_washingtonpost -> 8075_thewashingtonpost
	8380_houstonchronicle -> 8380_thehoustonchronicle

humanities renaming:

	nomatch -> no-exact-match
	
	144574_daytondailynews -> 144574_daytondailynewsohio
	145252_themoscowtimes -> DELETE
	148909_thedailyrecord -> 148909_thedailyrecordbaltimore
	151550_dailynewsnewyork -> 151550_dailynews
	162642_thewyomingtribuneeagle

...for the JSON files within the zips, their rename pattern may double the index number, e.g.

	144574_144574_daytondailynews

