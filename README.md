# NLC-scraper

To get the count of number of shows and scripts from all years:
```
python .\nlc-script-database-master\scraper\run_script_scraper.py
```

To get the count of number of shows and scripts from year 2021:
```
python .\nlc-script-database-master\scraper\run_scrape2021.py
```

To generate text files of scripts with titles given as a csv file with columns as title, script_type, year, season, episode
```
python .\nlc-script-database-master\scraper\run_scrape_csv.py
```

To generate text files of scripts with titles given as zip folders from opensubtitles use download.py
```
python .\download.py
```
After running the above command use run_pg_import_creator.py and then use run_script_importer.py to upload the subtitles to the NLC DB


To correct the dates in the DB use date-corrector given an excel sheet with columns - 'Program', 'Season to Move', 'Move From', 'Move To'
```
python .\data-corrector.py
```

Scrape viewership from mms.tveyes.com give an excel sheet with column - 'thumbnail href'
```
python .\scrape_viewership.py
```

