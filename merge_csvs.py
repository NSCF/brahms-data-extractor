# joins a set of csvs in a directory into one file
# expects one file to have all the headers found in the other csvs. 
# see compare_csv_headers.py
# note that this scripts outputs all results to file called all.csv, so if that already exists it will be overwritten

import os, csv

csv_dir = r"E:\Herbarium imaging\NU\CPF_RDE\csv"
csv_with_all_headers = r"dicots10.csv"
source_field = "SOURCE" # the name of the field to add for the source file

all_records = []
all_fields = []

print('reading csvs')

with open(os.path.join(csv_dir, csv_with_all_headers), 'r', encoding='UTF8', errors='ignore', newline='') as f:
  reader = csv.DictReader(f)
  for record in reader:
    record[source_field] = csv_with_all_headers
    all_records.append(record)

all_fields = all_records[0].keys()

files = os.listdir(csv_dir)
csvs = list(filter(lambda x: x.lower().endswith('.csv'), files))

for csv_file in csvs:
  
  if csv_file == csv_with_all_headers:
    continue

  with open(os.path.join(csv_dir, csv_file), 'r', encoding='UTF8', errors='ignore', newline='') as f:
    reader = csv.DictReader(f)
    for record in reader:
      mapped = {}
      for field in all_fields:
        if field in record:
          mapped[field] = record[field]
        else:
          mapped[field] = None
      mapped[source_field]
      all_records.append(mapped)

print('writing out results')
with open(os.path.join(csv_dir, 'all.csv'), 'w', encoding='UTF8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, all_fields)
    writer.writeheader()
    writer.writerows(all_records)

print('all done...')