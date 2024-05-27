# compares headers in a set of csv files in a directory and outputs those not shared with all others
# use this as prep for merge_csvs

import os
import csv

csv_dir = r"E:\Herbarium imaging\NU\CPF_RDE\csv"

files = os.listdir(csv_dir)
csvs = list(filter(lambda x: x.lower().endswith('.csv'), files))

if len(csvs) == 0:
  print('No csvs found in the specified directory')
  exit()

headers = {}
print('reading csvs')
for csv_file in csvs:
  with open(os.path.join(csv_dir, csv_file), 'r', encoding='UTF8', errors='ignore', newline='') as f:
    reader = csv.DictReader(f)
    first = next(reader)
    csv_headers = list(first.keys())
    headers[csv_file] = csv_headers

first_set = set(list(headers.values())[0])
rest = list(map(lambda x: set(x), list(headers.values())[1:]))
common_headers = first_set.intersection(*rest)

counter = 0
for file, file_headers in headers.items():
  additional = set(file_headers) - common_headers
  missing = common_headers - set(file_headers)

  if missing:
    counter += 1
    print(file, 'is missing', str(missing))
  
  if additional:
    counter += 1
    print(file, 'has additional', str(additional))

if counter == 0: #the headers are all the same
  print('The headers are all the same')





