# outputs counts per file for a folder of csv files

from os import path, listdir
import csv

csvDir = r'D:\NSCF Data WG\Specify migration\PRU\PRUBRAHMS7\PRU\openrefine csv'

files = listdir(csvDir)
csvs = list(filter(lambda x: x.lower().endswith('.csv'), files))
i = 0

for csvFile in csvs:
    with open(path.join(csvDir, csvFile), 'r', encoding='UTF8', errors='ignore', newline='') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            count += 1

        print(csvFile, 'has', count, 'records')
    
    

