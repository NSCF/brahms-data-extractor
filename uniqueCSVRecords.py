# adjust the code below depending on requirements

import dataset
from os import path
import csv
from progress.bar import Bar

csvPath = r'C:\Users\Ian Engelbrecht\Downloads'
csvFile = r'PRU-allDataExtracted-OpenRefine_getUniqueLocalityCodes.csv'
outputFile = r'PRU-allDataExtracted_UniqueLocalityCodes.csv'
fields = ['country', 'major', 'minor', 'gazlocality']
totalRecords = 66000

db = dataset.connect('sqlite:///records.sqlite')
table = db['records']
table.drop() #remove and recreate
table = db['records']
for field in fields:
  table.create_column(field, db.types.string)

print('adding data to sqlite, this may take a few moments...')
bar = Bar('Loading', max=totalRecords)
with open(path.join(csvPath, csvFile), 'r', encoding='UTF8', errors="ignore") as f:
  reader = csv.DictReader(f)
  for row in reader:
    data = dict()
    for field in fields:
      data[field] = row[field]
    table.insert(data)
    bar.next()
bar.finish()

print('getting unique rows')
sql = 'SELECT DISTINCT country, major, minor, gazlocality from records where major REGEXP \'\d+\' or gazlocality REGEXP \'^\d+$\''
with open(path.join(csvPath, outputFile), 'w', encoding='UTF8', newline='') as f:
  writer = csv.writer(f)
  headersAdded = False
  for row in db.query(sql):
    if not headersAdded:
      writer.writerow(row.keys())
      headersAdded = True
    writer.writerow(row.values())

print('all done')