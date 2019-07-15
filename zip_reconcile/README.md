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

	6742_newyorktimes_ -> 6742_thenewyorktimes_
	8006_losangelestimes_ -> 8006_thelatimes_
	8075_washingtonpost_ -> 8075_thewashingtonpost_
	8380_houstonchronicle_ -> 8380_thehoustonchronicle_

humanities renaming:

	nomatch -> no-exact-match
	no-match -> no-exact-match

	144574_daytondailynews_ -> 144574_daytondailynewsohio_
	148909_thedailyrecord_ -> 148909_thedailyrecordbaltimore_
	151550_dailynewsnewyork_ -> 151550_dailynews_
	164207_thenewyorkpost_ -> 164207_newyorkpost_
	164263_thebismarktribune_ -> 164263_bismarcktribune_
	168851_tapokacapitaljournal_ -> 168851_topekacapitaljournal_
	256478_argusleadersiouxfallssouthdakota_ -> 256478_argusleadersouthdakota_
	313177_abc_ -> 313177_abcspain_
	314595_finnishamericanreporter_ -> 314595_thefinnishamericanreporter_
	316023_theamericanconservative_ -> 316023_americanconservative_
	381159_gulftimes_ -> 381159_gulftimesqatar_
	387687_thejewishstar_ -> 387687_thejewishstarnewyork_
	388127_theasianpacificpost_ -> 388127_theasianpacificpostvancouverbritishcolumbia_
	418672_cosmopolitanus_ -> 418672_cosmopolitan_
  8006_losangelestimes_ -> 8006_thelatimes_
	amandala_humanities.zip -> chomp-amandala_humanities.zip
	andina-ingles_humanities.zip -> chomp-andina-ingles_humanities.zip
	banderasnews_humanities.zip -> chomp-banderasnews_humanities.zip
	banderasnews_liberal_arts.zip -> chomp-banderasnews_liberal_arts.zip
	bolivianexpress-org_humanities.zip -> chomp-bolivianexpress-org_humanities.zip
	Brazzil_humanities.zip -> chomp-Brazzil_humanities.zip
	Brazzil_liberalarts.zip -> chomp-Brazzil_liberalarts.zip
	ProQuestDocuments_wsj_ -> ProQuestDocuments_thewallstreetjournal_
	ProQuest_Humanit_ -> ProQuest_humanities_
	Reddit-All-Humanities-2006-2018_.zip -> reddit-all-humanities-2006-2018_.zip
	Reddit-All-Liberal-Arts-2006-2018_.zip -> reddit-all-liberal-arts-2006-2018_.zip
	Reddit-All-The-Arts-2006-2018.zip -> reddit-all-the-arts-2006-2018.zip

DELETE: DO DELETES FIRST
144574_daytondailynews_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
144574_daytondailynews_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31.zip
144574_daytondailynews_bodysingularhumanities_2015-01-01_2015-12-31(no-exact-match).zip
144574_daytondailynews_bodysingularhumanities_2015-01-01_2015-12-31.zip
144574_daytondailynews_bodysingularhumanities_2016-01-01_2016-12-31(no-exact-match).zip
144574_daytondailynews_bodysingularhumanities_2016-01-01_2016-12-31.zip
144574_daytondailynews_bodysingularhumanities_2017-01-01_2017-12-31(no-exact-match).zip
144574_daytondailynews_bodysingularhumanities_2017-01-01_2017-12-31.zip
144574_daytondailynews_bodysingularhumanities_2018-01-01_2018-12-31(no-exact-match).zip
144574_daytondailynews_bodysingularhumanities_2018-01-01_2018-12-31.zip
144579_saltlaketribune_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
144579_saltlaketribune_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_1997-01-01_1997-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_1998-01-01_1998-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_1999-01-01_1999-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2000-01-01_2000-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2001-01-01_2001-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2002-01-01_2002-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2003-01-01_2003-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2004-01-01_2004-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2005-01-01_2005-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2006-01-01_2006-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2007-01-01_2007-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2008-01-01_2008-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2009-01-01_2009-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2010-01-01_2010-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2011-01-01_2011-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2012-01-01_2012-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2013-01-01_2013-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2014-01-01_2014-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2015-01-01_2015-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2016-01-01_2016-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2017-01-01_2017-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_2018-01-01_2018-12-31.zip
162642_wyomingtribuneeagle_bodysingularhumanity_1997-01-01_1997-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_1998-01-01_1998-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_1999-01-01_1999-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2000-01-01_2000-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2001-01-01_2001-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2002-01-01_2002-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2003-01-01_2003-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2004-01-01_2004-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2005-01-01_2005-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2006-01-01_2006-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2007-01-01_2007-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2008-01-01_2008-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2009-01-01_2009-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2010-01-01_2010-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2011-01-01_2011-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2012-01-01_2012-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2013-01-01_2013-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2014-01-01_2014-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2015-01-01_2015-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2016-01-01_2016-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2017-01-01_2017-12-31(no-exact-match).zip
162642_wyomingtribuneeagle_bodysingularhumanity_2018-01-01_2018-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2004-01-01_2004-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2004-01-01_2004-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2005-01-01_2005-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2005-01-01_2005-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2006-01-01_2006-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2006-01-01_2006-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2009-01-01_2009-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2009-01-01_2009-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2010-01-01_2010-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2010-01-01_2010-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2011-01-01_2011-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2012-01-01_2012-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2012-01-01_2012-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2013-01-01_2013-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2013-01-01_2013-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2014-01-01_2014-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2014-01-01_2014-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2015-01-01_2015-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2016-01-01_2016-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2016-01-01_2016-12-31.zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
164207_thenewyorkpost_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_2017-01-01_2017-12-31.zip
164282_deseretmorningnews_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
164282_deseretmorningnews_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_1998-01-01_1998-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_1998-01-01_1998-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_1999-01-01_1999-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_1999-01-01_1999-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2000-01-01_2000-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2001-01-01_2001-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2001-01-01_2001-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2002-01-01_2002-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2002-01-01_2002-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2003-01-01_2003-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2003-01-01_2003-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2004-01-01_2004-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2004-01-01_2004-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2005-01-01_2005-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2005-01-01_2005-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2006-01-01_2006-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2006-01-01_2006-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2007-01-01_2007-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2007-01-01_2007-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2008-01-01_2008-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2008-01-01_2008-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2009-01-01_2009-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2009-01-01_2009-12-31.zip
168851_tapokacapitaljournal_bodypluralhumanities_2010-01-01_2010-12-31(no-exact-match).zip
168851_tapokacapitaljournal_bodypluralhumanities_2010-01-01_2010-12-31.zip
172244_172244_universitywire_bodypluralhumanitiesorhleadpluralhumanities_.zip
256478_argusleader_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
256478_argusleader_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31.zip
158208_koreaherald_bodyliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
158208_koreaherald_bodyliberalpre1pluralarts_2017-01-01_2017-12-31.zip
158440_thedailyoklahoman_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
158440_thedailyoklahoman_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31.zip
158440_thedailyoklahoman_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
158440_thedailyoklahoman_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31.zip
163823_chicagodailyherald_bodyliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
163823_chicagodailyherald_bodyliberalpre1pluralarts_2017-01-01_2017-12-31.zip
164207_newyorkpost_bodyliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
164207_newyorkpost_bodyliberalpre1pluralarts_2017-01-01_2017-12-31.zip
247189_thephiladelphiainquirer_bodyliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
247189_thephiladelphiainquirer_bodyliberalpre1pluralarts_2017-01-01_2017-12-31.zip
247246_thephiladelphiadailynewspa_bodyliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
247246_thephiladelphiadailynewspa_bodyliberalpre1pluralarts_2017-01-01_2017-12-31.zip
317177_dailycamera_bodyliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
317177_dailycamera_bodyliberalpre1pluralarts_2017-01-01_2017-12-31.zip
6742_thenewyorktimes_bodyliberalpre1pluralarts_2017-01-01_2017-12-31(no-exact-match).zip
8109_dailytelegraphlondon_arts_2017-01-01_2017-12-31.zip
8109_dailytelegraphlondon_bodypluralartsorhleadpluralarts_2017-01-01_2017-12-31(no-exact-match).zip
8109_dailytelegraphlondon_bodypluralartsorhleadpluralarts_2017-01-01_2017-12-31.zip
8113_newsdaynewyork_bodypluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
8113_newsdaynewyork_bodypluralhumanities_2017-01-01_2017-12-31.zip
8113_newsdaynewyork_bodypluralhumanities_2018-01-01_2018-12-31(no-exact-match).zip
8113_newsdaynewyork_bodypluralhumanities_2018-01-01_2018-12-31.zip
8384_startribune_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31(no-exact-match).zip
8384_startribune_bodypluralhumanitiesorhleadpluralhumanities_2017-01-01_2017-12-31.zip
ApplyingToCollege.zip
chomp_nea-today_humanities_2000-01-01_2020-01-01_no-match(1).zip
chomp_new-left-review_humanities_2000-01-01_2020-01-01_no-match(1).zip
chomp_newsone_humanities_2000-01-01_2020-01-01(1).zip
chomp_newsone_humanities_2000-01-01_2020-01-01_nomatch(1).zip
chomp_occidental-dissent_humanities_2000-01-01_2020-01-01_nomatch.zip
chomp_occidental-observer_humanities_2000-01-01_2020-01-01_nomatch.zip
Corpus-A-Comparison.zip
humanities-vs-stem.zip
_preprocessing_log.csv
_timings.txt
we1s-notes-all.zip
we1s-website.zip
_team10_webscrape_data.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_1998-01-01_1998-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_1998-01-01_1998-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_1999-01-01_1999-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_1999-01-01_1999-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2000-01-01_2000-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2000-01-01_2000-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2001-01-01_2001-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2001-01-01_2001-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2002-01-01_2002-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2002-01-01_2002-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2003-01-01_2003-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2003-01-01_2003-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2004-01-01_2004-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2004-01-01_2004-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2005-01-01_2005-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2005-01-01_2005-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2006-01-01_2006-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2006-01-01_2006-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2007-01-01_2007-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2007-01-01_2007-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2008-01-01_2008-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2008-01-01_2008-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2009-01-01_2009-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2009-01-01_2009-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2010-01-01_2010-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2011-01-01_2011-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2011-01-01_2011-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2012-01-01_2012-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2012-01-01_2012-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2013-01-01_2013-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2013-01-01_2013-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2014-01-01_2014-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2014-01-01_2014-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2015-01-01_2015-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2015-01-01_2015-12-31.zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2016-01-01_2016-12-31(no-exact-match).zip
168851_unknowntitle_bodypluralhumanitiesorhleadpluralhumanities_2016-01-01_2016-12-31.zip


FILES WITH EXACT DUPLICATE ZIP NAMES: ONLY ONE SHOULD BE DELETED
* chomp_21st-century-principal_humanities_2000-01-01_2020-01-01.zip
* chomp_raw-story_humanities_2000-01-01_2020-01-01_nomatch.zip
* chomp_redstate_humanities_2000-01-01_2020-01-01.zip
* chomp_slate-magazine_humanities_2000-01-01_2020-01-01.zip
* chomp_the-christian-science-monitor_humanities_2000-01-01_2020-01-01_nomatch.zip
* chomp_the-conversation_humanities_2000-01-01_2020-01-01_nomatch.zip
* chomp_the-conversation_humanities_2000-01-01_2020-01-01.zip
* chomp_the-daily-beast_humanities_2000-01-01_2020-01-01.zip
* chomp_the-daily-beast_humanities_2000-01-01_2020-01-01_nomatch.zip
* chomp_the-daily-caller_humanities_2000-01-01_2020-01-01.zip
* chomp_the-nevada-independent_humanities_2000-01-01_2020-01-01.zip
* chomp_the-pueblo-chieftain_humanities_2000-01-01_2020-01-01_nomatch.zip
* chomp_the-root_humanities_2000-01-01_2020-01-01_nomatch.zip
* chomp_the-verge_humanities_2000-01-01_2020-01-01.zip
* chomp_upworthy_humanities_2000-01-01_2020-01-01.zip
* chomp_vice-news_humanities_2000-01-01_2020-01-01.zip
* chomp_village-voice_humanities_2000-01-01_2020-01-01.zip
* chomp_village-voice_humanities_2000-01-01_2020-01-01_nomatch.zip
* chomp_worldnetdaily_humanities_2000-01-01_2020-01-01.zip
* chomp_worldnetdaily_humanities_2000-01-01_2020-01-01_nomatch.zip


ON HARBOR BUT NOT ON BAREMETAL?:
2019-01-31-Reddit-I-Majored-In-myzip.zip

...for the JSON files within the zips, their rename pattern may double the index number, e.g.

	144574_144574_daytondailynews
