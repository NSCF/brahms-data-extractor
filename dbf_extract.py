# extract all BRAHMS tables to csv files

from os import path, listdir, remove
from dbfread import DBF
import csv
import re

dbdir = r'E:\PRUBRAHMS7\PRU\DATABASE'
outputdir = r'E:\PRUBRAHMS7\PRU\temp'

dbfs = [f for f in listdir(dbdir) if path.isfile(path.join(dbdir, f)) and f.lower().endswith('dbf')]

for dbf in dbfs:
  recordCount = 0
  csvfile = re.sub('\.dbf$', '.csv', dbf, flags=re.I)
  with open(path.join(outputdir, csvfile), 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    fieldsadded = False
    for record in DBF(path.join(dbdir, dbf), char_decode_errors='ignore'):
      if not fieldsadded:
        fields = record.keys()
        writer.writerow(fields)
        fieldsadded = True
      vals = record.values()
      writer.writerow(vals)
      recordCount = recordCount + 1

  if recordCount == 0:
    # print('no records in', csvfile)
    remove(path.join(outputdir, csvfile))
  else:
    print(recordCount, 'records transfered from', csvfile)

print('all done!')
