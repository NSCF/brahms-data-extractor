from mysql.connector import connect, Error
from os import path, listdir
import csv
import re
import json

csvdir = r'E:\PRUBRAHMS7\PRU\csv' #there must be nothing else in this directory
schemasqldir = r'E:\PRUBRAHMS7\PRU'
schemasqlfile = r'pru brahms.sql'
databasename ='pru'
tables = [
  'people',
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

errs = {}

try:
  with connect(
    host="localhost",
    user="root",
    password="root"
  ) as connection:
    with connection.cursor() as cursor:
     
      #now we need the list of tables so we can check it later
      cursor.execute(f'use {databasename}')
      # cursor.execute('show tables')
      # tables = cursor.fetchall()
      # tables = list(map(lambda x: str(x).replace('(', '').replace(')', '').replace("'", '').replace(',',''), tables))

      #read in the data
      csvs = listdir(csvdir) 
      for table in tables:

        print('loading data for', table)

        csvFile = table + '.csv'
        if not path.isfile(path.join(csvdir, csvFile)):
          print('OOOPS!!!!', csvFile, 'does not exist!!!')
          exit()

        #get the fields
        cursor.execute(f'show columns in {table}')
        result = cursor.fetchall()
        fields = list(map(lambda x: x[0], result))
        types = list(map(lambda x: x[1], result))

        records_to_insert = []
        with open(path.join(csvdir, csvFile), 'r', encoding='UTF8', errors='ignore') as f:
          reader = csv.DictReader(f)
          for row in reader:
            data = []
            rowkeys = row.keys()
            for index, field in enumerate(fields):
              targetkey = next(x for x in rowkeys if x.lower() == field or x.upper() == field)
              val = row[targetkey]
              val = val.strip()
              if val == '':
                val = None
              if val is not None:
                dt = types[index]
                if dt.startswith('int'):
                  val = int(val)
                elif dt.startswith('double'):
                  val = float(val)

              data.append(val)
            
              #records_to_insert.append(tuple(data))

            ss = ", ".join(["%s"] * len(fields))
            insertsql = f'insert into {table} values ({ss})'
            try:
              cursor.execute(insertsql, data)
            except Error as e: 
              #print('got an error in', table)
              if table in errs:
                errs[table].append(row)
              else:
                errs[table] = [row]

        
        connection.commit()

except Error as e:
  print(e)

jsondata = json.dumps(errs, indent=2)
with open('errors.json', 'w') as f:
  f.write(jsondata)

print('all done')
