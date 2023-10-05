#get a list of unique values in a column from a csv file

import csv
from os import path

csvDir = r'C:\Users\Ian Engelbrecht\Downloads'
csvFile = 'uniqueNames.csv'
csvFieldName = 'uniques'
outputCSVFile = 'uniqueNames2.csv'

print('getting unique vals from', csvFieldName)
vals = set()
with open(path.join(csvDir, csvFile), 'r', encoding='UTF8', errors='ignore') as f:
  reader = csv.DictReader(f)
  for row in reader:
    if csvFieldName in row:
      val = row[csvFieldName]
      if val != None and val != '':
        vals.add(val)
    else:
      print('Oops!', csvFieldName, 'does not exist in', csvFile)

if len(vals) > 0:
  print('writing out uniques')
  with open(path.join(csvDir, outputCSVFile), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['uniques'])
    
    for val in vals:
      writer.writerow([val])

  print('all done')

else:
  print('no values found in', csvFieldName)
