from os import path, walk, listdir, remove, mkdir
from dbfread import DBF
import csv
import re

#For Skukuza we need a custom parser - and we'll just keep it...
from customParsers import genericParser

#first get the csv files from BRAHMS dbf files
dbdir = r'E:\Herbarium imaging\NU\CPF_RDE' #The BRAHMS database folder
outputdir = r'E:\Herbarium imaging\NU\CPF_RDE\csv'

if not path.isdir(outputdir):
  mkdir(outputdir)

for root, dir_names, file_names in walk(dbdir):
  for f in file_names:
    if f.lower().endswith('.dbf'):
      dbf = path.join(root, f)
      recordCount = 0
      csvfile = re.sub('\.dbf$', '.csv', f, flags = re.I)
      with open(path.join(outputdir, csvfile), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        fieldsadded = False
        for record in DBF(dbf, char_decode_errors='ignore', parserclass=genericParser):
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