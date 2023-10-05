# after everything is loaded in the db, we can extract the fields we need as our final dataset
# note this uses extract_data.sql, see that file to see what you'll get

from mysql.connector import connect, Error
from os import path
import csv
from progress.bar import Bar
import time

dbhost ='localhost'
dbuser = 'root'
dbpwd = 'root'

dbname = 'bnrh_taxonomy'
csvDestDir = r'D:\NSCF Data WG\Data\BNRH'
outputFileName = 'taxonomyExtract.csv'  # or allDataExtracted.csv or prumAdditionalDets.csv

#these two must match...
extype = 'tax' # data | dets | tax
sqlfile = 'extract_taxonomy.sql'

#SCRIPT
#first get the sql
#note it has no search params
with open(sqlfile, 'r') as sqlfile:
  sql = sqlfile.read()

try:
  with connect(
    host = dbhost,
    user = dbuser,
    password = dbpwd,
    sql_mode ='TRADITIONAL'
  ) as connection:
    with connection.cursor(dictionary=True) as cursor:
    
      #now we need the list of tables so we can check it later
      cursor.execute(f'use {dbname}')

      #get a count so we can show progress
      if extype == 'data':
        cursor.execute('select count(*) as cnt from specimens')
        result = cursor.fetchall()
        for row in result:
          count = row['cnt']

      #read the db
      if extype == 'data':
        bar = Bar('Extracting', max=count)
      cursor.execute(sql)
      firstrecord = cursor.fetchone()
      fields = firstrecord.keys()
      start = time.time()
      if extype == 'data':
        bar.next()
      
      with open(path.join(csvDestDir, outputFileName), 'w', encoding='UTF8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fields)
        writer.writeheader()
        writer.writerow(firstrecord)

        for row in cursor:
          writer.writerow(row)
          if extype == 'data':
            bar.next()

      if extype == 'data':
        bar.finish()

      end = time.time()
      millis = end * 1000 - start * 1000

      seconds=int(millis/1000)%60
      minutes=int(millis/(1000*60))%60
      hours=int(millis/(1000*60*60))%24

      print (f'all done in {hours}h{minutes}m{seconds}s')
      exit(0)

except Error as e:
  print(e)