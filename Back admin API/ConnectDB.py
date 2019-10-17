# -*- coding: utf-8 -*- #
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database = 'test'
)
if (mydb):
    print 'connect success'
else:
    print 'Error'

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM bbb")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
    dict = {'name':x}
    print(dict)
