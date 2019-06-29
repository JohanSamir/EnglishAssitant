#References:
#1. https://medium.com/analytics-vidhya/programming-with-databases-in-python-using-sqlite-4cecbef51ab9"
#2. It is not necessary to instal: sudo apt-get install sqlitebrowser

import pandas as pd
import sqlite3

#------------------------------------------#

sqlite_file = '/home/johan/repos/GitHub/EnglishAssitant/datafile'    # name of the sqlite database file
# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
print("Opened database successfully")

#------------------------------------------#
for row in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(row)
    
#Exploratory Data Analysis
person_table = pd.read_sql_query("SELECT * FROM person", conn)
print("Dimension of Country Table is: {}".format(person_table.shape))
print(100*" ")
print(person_table.info())
#person_table
print(100*" ")
#------------------------------------------#
for row in c.execute('SELECT * FROM person'):
    print(row)
print(100*" ")
#------------------------------------------#
code = 'A'
c.execute("SELECT * FROM person WHERE firstname = '%s'" % code)
print(c.fetchone())