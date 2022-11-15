import psycopg2
from os import path, listdir
from os.path import isfile, join
import logging
from time import time, strftime
import pandas as pd
import tmdbsimple as tmdb
import re
tmdb.API_KEY = ''

class dbConnect:
  def __init__(self, db_info):
    self.db_info = db_info
    self.table_name = self.db_info['table_name']
    self.conn_str = "dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_password}'".format(
                    db_name=self.db_info['db_name'],
                    db_user=self.db_info['db_user'],
                    db_host=self.db_info['db_host'],
                    db_password=self.db_info['db_password']
                  ) 
    self.conn = None
    self.log_file = 'scriptimporter_{time}.log'.format(time=strftime('%Y-%m-%d %H-%M'))

    logging.basicConfig(filename=self.log_file, format='%(levelname)s: %(message)s', level=logging.DEBUG)
    
  
  def run_import_process(self):
    """Connect to the database and kick off the script import process.
    """
    start_time = time()

    try:
      logging.info('Starting import process')
      self.connect_to_db()
    except Exception as e:
      raise ValueError('Failed to connect to database with given information.' + str(e))

    self.cur.execute("""SELECT TITLE, YEAR FROM search_script where script_type = 'M' and title LIKE 'A%'""")
    res = self.cur.fetchall()
    df = []
    n = len(res)
    print(n)
    c=0
    for row in res:
        print(c)
        c+=1
        print(row)
        title = row[0]
        dates = re.findall(r'[(][\d]{4,4}[)]', title)
        if len(dates) > 0:
            # If a date in the format (####) exists then take the last one and remove from the title
            title = title[:-7]
        new = tmdb_movie_fetch(title,row[1])
        print(new)
        df.append(new) 
    df = pd.DataFrame(df, columns=['tmdb-title', 'title', 'year', 'genres', 'origin country', 'revenue'])
    df.to_excel("titles.xlsx",index=False, sheet_name="movies")
    
    self.conn.close()

    total_time = time() - start_time
    logging.info('Import process completed in {time} sec.'.format(time=total_time))
  
  def connect_to_db(self):
    """Connect to the postgres instance.
    """
    logging.info('Connecting to postgres')
    self.conn = psycopg2.connect(self.conn_str)
    self.conn.autocommit = True
    self.cur = self.conn.cursor()

def tmdb_movie_fetch(title, year):
    search = tmdb.Search()
    response = search.movie(query=title)
    res = []
    if len(search.results):
        for s in search.results:
            id = s['id']
            movie = tmdb.Movies(id)
            response = movie.info()
            if response['release_date'] and int(response['release_date'][:4]) == year:
                genres = []
                for genre_dict in response['genres']:
                    genres.append(genre_dict['name'])
                countries = []
                for countries_dict in response['production_countries']:
                    countries.append(countries_dict['name'])
                return [response['original_title'], title, year, genres, countries, response['revenue']]
                # print(response['original_title'], response['release_date'], response['genres'], response['production_countries'], response['revenue'])

def run_movies_fromdb(db_info):
  try:
    script_importer = dbConnect(db_info)
    print('Starting script import process')
    script_importer.run_import_process()
    print('Finished script import process')
  except Exception as e:
    print('An error occurred during import process: {error}'.format(error=str(e)))


if __name__ == '__main__':
  db_info = { 'db_name': 'ebdb', 'db_user': 'master', 'db_host': 'aa70q1acjlahr9.cqauetjzyrt7.us-west-1.rds.amazonaws.com', 'db_password': 'LearCenter', 'table_name': 'search_script'}

  # Engage!
  run_movies_fromdb(db_info)
