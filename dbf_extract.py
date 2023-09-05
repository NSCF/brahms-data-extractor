from os import path, listdir, remove, mkdir
from dbfread import DBF, FieldParser
import csv
import re

#For Skukuza we need a custom par
from customParsers import stringdates

#first get the csv files from BRAHMS dbf files
dbdir = r'D:\BACKUP BRAHMS_31 08 2021\BRAHMS_KNP_DATA\myrdefiles' #The BRAHMS database folder
outputdir = r'C:\temp\SkukuzaBRAHMS/rde'

if not path.isdir(outputdir):
  mkdir(outputdir)

dbfs = [f for f in listdir(dbdir) if path.isfile(path.join(dbdir, f)) and f.lower().endswith('dbf')]

for dbf in dbfs:
  recordCount = 0
  csvfile = re.sub('\.dbf$', '.csv', dbf, flags = re.I)
  with open(path.join(outputdir, csvfile), 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    fieldsadded = False
    for record in DBF(path.join(dbdir, dbf), char_decode_errors='ignore', parserclass=stringdates):
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

print('all done')