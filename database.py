#References:
#1. https://medium.com/analytics-vidhya/programming-with-databases-in-python-using-sqlite-4cecbef51ab9"
#2. It is not necessary to instal: sudo apt-get install sqlitebrowser

import pandas as pd
import sqlite3
import	numpy as np
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
#print("Dimension of Country Table is: {}".format(person_table.shape))
#print(100*" ")
#print(person_table.info())
#person_table
#print(100*" ")
#------------------------------------------#
for row in c.execute('SELECT * FROM person'):
    print(row)
#print(100*" ")
#------------------------------------------#
code = 'V'
c.execute("SELECT * FROM person WHERE firstname = '%s'" % code)
#print(c.fetchall())

code = 'A'
c.execute("SELECT * FROM person WHERE firstname = '%s'" % code)
#print(c.fetchone())
#------------------------------------------#

df = pd.DataFrame(person_table, columns=['id','firstname','lastname','stname','sstname','ssstname'])
# get the maximum value of the column 'Age'
idmax = df['id'].max()
#print(idmax)    
df.head()

#------------------------------------------#
adjectives = np.array(df.loc[df['firstname'] == 'A'])
lenadjec = len(adjectives)
Verbs = np.array(df.loc[df['firstname'] == 'V'])
lenverbs = len(Verbs)

print(100*" ")
print('------------------------------------------------')
again = input(" Do you want to start the test?: Yes: 1 No: 0  ")
while int(again) == 1:
	aV =  np.random.randint(0,lenadjec) 
	aA =  np.random.randint(0,lenverbs) 

	print('adjectives',adjectives[aA],'\nVerbs',Verbs[aV])
	print('------------------------------------------------')
	print(100*" ")
	again = input(" Do you want to do the test again?:Yes: 1 No: 0   ")


