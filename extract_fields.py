from mysql.connector import connect, Error
from os import path, listdir
import csv
import re
from funcs import create_db, make_row_data

dbhost ='localhost'
dbuser = 'root'
dbpwd = 'root'
dbname = 'pru'
schemasqldir = r'E:\PRUBRAHMS7\PRU'
schemasqlfile = r'pru brahms.sql'

#extract the fields we want from the csv files so we can clean them in OpenRefine
csvdir = r'E:\PRUBRAHMS7\PRU\csv' #there must be nothing else in this directory
outdir = r'E:\PRUBRAHMS7\PRU\trimmed_csvs'

try:
  create_db(dbhost, dbuser, dbpwd, dbname, schemasqldir, schemasqlfile)
except Error as e:
  print(e)
  exit()

if csvdir == outdir:
  raise Exception("input and output directories cannot be the same")

try:
  with connect(
    host = dbhost,
    user = dbuser,
    password = dbpwd
  ) as connection:
    with connection.cursor() as cursor:
      
      cursor.execute(f'use {dbname}')
      cursor.execute('show tables')
      dbtables = cursor.fetchall()
      dbtables = list(map(lambda x: x[0].lower(), dbtables))

      csvs = listdir(csvdir) 

      for csvFile in csvs:

        table = re.sub('\.csv$', '', csvFile, flags = re.I)
        if table.lower() in dbtables:
        
          print('getting data for', table)
          #get the fields
          cursor.execute(f'show columns in {table}')
          result = cursor.fetchall()
          fields = list(map(lambda x: x[0], result))
          types = list(map(lambda x: x[1], result))

          with open(path.join(outdir, csvFile), 'w',  encoding='UTF8', newline='') as outf:

            writer = csv.writer(outf)
            writer.writerow(fields)

            with open(path.join(csvdir, csvFile), 'r', encoding='UTF8', errors='ignore') as f:
              reader = csv.DictReader(f)
              for row in reader:
                data = make_row_data(row, fields, types)
                writer.writerow(data)

except Error as e:
  print(e)

print('all done')