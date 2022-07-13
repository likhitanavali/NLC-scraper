from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from zipfile import ZipFile
import os
import scraper_constants
import time

url = "https://www.opensubtitles.org/en/search/sublanguageid-eng/searchonlymovies-on/movieyearsign-1/movieyear-2021"
page = urlopen(url)
soup = BeautifulSoup(page, 'lxml')
print(soup)
titles_soup = soup.findAll('tr', {'class':
                ['change even expandable', 'change odd expandable']})
title_links = {}
print(titles_soup)
for title_tag in titles_soup:
    title = title_tag.select("td:nth-of-type(1) a")[0]['title'].replace("subtitles - ","")
    link = title_tag.select("td:nth-of-type(5) a[href]")[0]['href']
    title_links[title] = link

print(title_links)
for title in title_links.keys():
    try:
        urlretrieve("https://www.opensubtitles.org"+title_links[title], "file.zip")
    except Exception as e:
        print(e)
        if e.code == 429:
            time.sleep(5)
            urlretrieve("https://www.opensubtitles.org"+title_links[title], "file.zip")
    zf = ZipFile('file.zip', 'r')
    zf.extractall('D:/Spring22/RA/nlc-script-database-master/tools/raw_data/' + scraper_constants.clean_script_title(title))
    zf.close()
    os.remove("file.zip")
