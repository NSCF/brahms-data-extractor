from mysql.connector import connect, Error
from os import path, listdir
import csv
import json
import time
import re
from funcs import create_db, make_row_data

dbhost ='localhost'
dbuser = 'root'
dbpwd = 'root'
dbname = 'bnrh_taxonomy'
schemasqldir = r'D:\NSCF Data WG\Data\BNRH'
schemasqlfile = r'BRAHMS taxonomy.sql'
csvdir = r'D:\NSCF Data WG\Data\BNRH\csv_taxonomy_openrefine' #there must be nothing else in this directory

#the table order
tableorder = [
  'peopleview',
  'country',
  'gaz', 
  'family',
  'genus',
  'species',
  'ih',
  'typecategories',
  'botrecordcats',
  'collections',
  'colllink',
  'specimens',
  'dethistory'
]

#clear previous db
try:
  create_db(dbhost, dbuser, dbpwd, dbname, schemasqldir, schemasqlfile)
except Error as e:
  print(e)
  exit()

errs = {}

try:
  with connect(
    host = dbhost,
    user = dbuser,
    password = dbpwd,
    sql_mode ='TRADITIONAL'
  ) as connection:
    with connection.cursor() as cursor:
    
      #now we need the list of tables so we can check it later
      cursor.execute(f'use {dbname}')
      # cursor.execute('show tables')
      # tables = cursor.fetchall()
      # tables = list(map(lambda x: str(x).replace('(', '').replace(')', '').replace("'", '').replace(',',''), tables))

      start = time.time()
      #read in the data
      csvs = listdir(csvdir) 
      for table in tableorder:

        csvFiles = [csvFile for csvFile in csvs if re.sub('\.csv$', '', csvFile, flags = re.I).split('-')[0].lower() == table.lower()]
        if len(csvFiles) > 0:
          csvFile = csvFiles[0]
        else:
          print()
          print('no csv file found for', table)
          continue
        
        #this should not be possible!
        if not path.isfile(path.join(csvdir, csvFile)):
          print('OOOPS!!!!', csvFile, 'does not exist!!!')
          exit()

        #get the fields
        cursor.execute(f'show columns in {table}')
        result = cursor.fetchall()
        fields = list(map(lambda x: x[0], result))
        types = list(map(lambda x: x[1], result))

        with open(path.join(csvdir, csvFile), 'r', encoding='UTF8', errors='ignore') as f:
          reader = csv.DictReader(f)
          loadcount = 0
          errcount = 0
          print()
          for row in reader:
            data = make_row_data(row, fields, types)
            ss = ", ".join(["%s"] * len(fields))
            insertsql = f'insert into {table} values ({ss})'
            try:
              cursor.execute(insertsql, data)
              loadcount += 1
            except Error as e: 
              #print('got an error in', table)
              if table in errs:
                errs[table].append(row)
              else:
                errs[table] = [row]
              errcount += 1

          print(loadcount, 'records loaded for', table)
          if errcount:
            print(errcount, 'errors for', table)
        
        connection.commit()

      end = time.time()
      millis = end * 1000 - start * 1000

      seconds=int(millis/1000)%60
      minutes=int(millis/(1000*60))%60
      hours=int(millis/(1000*60*60))%24

      print (f'data loaded in {hours}h{minutes}m{seconds}s')

except Error as e:
  print(e)

print()
print('writing out error.json file')
jsondata = json.dumps(errs, indent=2)
with open('errors.json', 'w') as f:
  f.write(jsondata)

print()
print('all done')