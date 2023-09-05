#for the Skukuza dataset there are several rde files which appear not to have been transfered to the main database, so...

#they were were first extracted with dbf_extract.py
from os import path, listdir, mkdir
import csv

csvDir = r'C:\temp\SkukuzaBRAHMS\rde'
outDir = r'C:\temp\SkukuzaBRAHMS\rde\notinbrahms'
specimensDir = r'C:\Users\Ian Engelbrecht\Downloads'
specimensFile = r'Skukuza-BRAHMS-specimens-OpenRefine.csv'
specimensBarcodeField = 'Barcode'


#get the barcodes from specimens as a list
print('getting captured specimen barcodes')
captured_barcodes = []
with open(path.join(specimensDir, specimensFile), 'r', encoding='UTF8', errors='ignore') as f:
  reader = csv.DictReader(f)
  for row in reader:
    if specimensBarcodeField in row:
      captured_barcodes.append(row[specimensBarcodeField].strip().upper())
    else:
      print('no field named', specimensBarcodeField, 'in', specimensFile)
      exit()

#make the output directory if it doesn't exist
if not path.isdir(outDir):
  mkdir(outDir)

#get the rde csv files
csvFiles = filter(lambda x: x.lower().endswith('.csv'), listdir(csvDir)) 

#and process them
outputCount = 0
for csvFile in csvFiles:
  
  #get those not captured
  print('checking', csvFile)
  not_captured = []  
  with open(path.join(csvDir, csvFile), 'r', encoding='UTF8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
      if 'BARCODE' in row:
        barcode = row['BARCODE'].strip().upper()
        if barcode not in captured_barcodes:
          not_captured.append(row)
      else:
        print('BARCODE field does not exist in', csvFile)
        break

  #if we have not captured then write them out
  if len(not_captured) > 0:
    print(len(not_captured), 'not captured')
    outputCount += len(not_captured)
    fields = not_captured[0].keys()
    with open(path.join(outDir, csvFile), 'w', encoding='UTF8', newline='') as f:
      writer = csv.DictWriter(f, fields)
      writer.writeheader()
      writer.writerows(not_captured)

print(outputCount, 'total records not captured')
print('all done...')


  




