from mysql.connector import connect, Error
from os import path, listdir, remove
from dbfread import DBF
import csv
import json
import re


#use dbdiagram.io to create the database schema, which this uses
def create_db(dbhost, dbuser, dbpwd, databasename, schemadir, schemafile):
  try:
    with connect(
      host = dbhost,
      user = dbuser,
      password = dbpwd
    ) as connection:
      with connection.cursor() as cursor:
          
          cursor.execute(f'DROP DATABASE IF EXISTS {databasename} ')
          cursor.execute(f'CREATE DATABASE {databasename}')
          cursor.execute(f'USE {databasename}')

          print('creating database...')
          with open(path.join(schemadir, schemafile), 'r') as f:
            schemasql = f.read()
            cursor.execute(schemasql) 

  except Error as e:
    raise e
  
  print('all done')
  


  



def make_row_data(csvRowDict, fields, types):
  data = []
  rowkeys = csvRowDict.keys()
  for index, field in enumerate(fields):
    targetkey = next(x for x in rowkeys if x.lower() == field or x.upper() == field)
    val = csvRowDict[targetkey]
    val = val.strip()
    if val == '':
      val = None
    if val is not None:
      try:
        dt = types[index]
        if dt.startswith('int'):
          val = int(val)
        elif dt.startswith('double'):
          val = float(val)
      except Error as e:
        raise e

    data.append(val)

  return data