#imports data from csv files into mysql
#use dbdiagram.io to create the database schema, which this uses
#this is a messy mix of mysql and dataset, but that's what it is for now...

from mysql.connector import connect, Error
from os import path, listdir
import csv

csvdir = r'E:\PRUBRAHMS7\PRU\csv' #there must be nothing else in this directory
schemasqldir = r'E:\PRUBRAHMS7\PRU'
schemasqlfile = r'pru brahms.sql'
databasename ='pru'

try:
  with connect(
    host="localhost",
    user="root",
    password="root"
  ) as connection:
    with connection.cursor() as cursor:
        
        cursor.execute(f'DROP DATABASE IF EXISTS {databasename} ')
        cursor.execute(f'CREATE DATABASE {databasename}')
        cursor.execute(f'USE {databasename}')

        print('creating database...')
        with open(path.join(schemasqldir, schemasqlfile), 'r') as f:
           schemasql = f.read()
           cursor.execute(schemasql) 

except Error as e:
  print(e)

print('all done')



