from os import path, walk, listdir, remove, mkdir
from dbfread import DBF, FieldParser
import csv
import re

#For Skukuza we need a custom par
from customParsers import stringdates

#first get the csv files from BRAHMS dbf files
dbdir = r'D:\NSCF Data WG\Data\Moss\Moss Herbarium Database\NSCF Data capture' #The BRAHMS database folder
outputdir = r'D:\NSCF Data WG\Data\Moss\Moss Herbarium Database\csv'

if not path.isdir(outputdir):
  mkdir(outputdir)

for root, dir_names, file_names in walk(dbdir):
  for f in file_names:
    if f.endswith('.dbf'):
      dbf = path.join(root, f)
      recordCount = 0
      csvfile = re.sub('\.dbf$', '.csv', f, flags = re.I)
      with open(path.join(outputdir, csvfile), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        fieldsadded = False
        for record in DBF(dbf, char_decode_errors='ignore', parserclass=stringdates):
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