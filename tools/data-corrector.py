from copy import deepcopy
import pandas as pd
import logging
import psycopg2
from time import strftime, time

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
    
  
  def check_tv_title(self, title, season, fromyear, toyear):
    # season = season[6:].strip(" ")
    # print("check-tv ", title, year, season)
    if title[-1] == '.':
       title = title[:-1]
    try:
      logging.info('Starting tv check')
      self.connect_to_db()
    except Exception as e:
      raise ValueError('Failed to connect to database with given information.' + str(e))

    self.cur.execute("SELECT TITLE, YEAR, SEASON, EPISODE, EPISODE_TITLE FROM search_script where script_type = 'T' and season = (%s) and year = (%s) and LOWER(title) LIKE LOWER(%s)",[str(int(season)), str(int(fromyear)), title])
    res = self.cur.fetchall()
    update_sql = """ UPDATE search_script
                SET YEAR = %s
                WHERE script_type = 'T' 
                and season = (%s) 
                and year = (%s) 
                and LOWER(title) LIKE LOWER(%s) 
                and episode = (%s) 
                and LOWER(episode_title) LIKE LOWER(%s)"""
    n = len(res)
    print(n, title)
    for row in res:
        titleDB, yearDB, seasonDB, episodeDB, eptitleDB = row
        # print(titleDB, yearDB, seasonDB, episodeDB, eptitleDB)
        self.cur.execute(update_sql, (str(int(toyear)), seasonDB, yearDB, titleDB, episodeDB, eptitleDB))
    
    self.conn.close()
    return True

  def connect_to_db(self):
    """Connect to the postgres instance.
    """
    logging.info('Connecting to postgres')
    self.conn = psycopg2.connect(self.conn_str)
    self.conn.autocommit = True
    self.cur = self.conn.cursor()

def change_date(data):
    db_info = { 'db_name': 'ebdb', 'db_user': 'master', 'db_host': '', 'db_password': '', 'table_name': 'search_script'}
    try:
        db = dbConnect(db_info)
        for i in range(0,len(data)):
            check = db.check_tv_title(data['Program'][i], data['Season to Move'][i], data['Move From'][i], data['Move To'][i])
    except Exception as e:
        print("Failed at dbconnect", e)

def main():
    data = pd.read_excel("NLC Script Database 2021 2022 Audit.xlsx", sheet_name="Year Change")
    data = data[['Program', 'Season to Move', 'Move From', 'Move To']]
    change_date(data)

if __name__ == "__main__":
    main()