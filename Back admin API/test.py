# -*- coding: utf-8 -*- #
from flask import Flask, request, jsonify, current_app, abort, send_from_directory, send_file,Response
import mysql.connector
import datetime
app = Flask(__name__,static_url_path='')
mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database='bookingsdb')


mycursor = mydb.cursor()
mycursor.execute("SELECT booking_id,room_id,date_checkin,date_checkout,days_number,payment FROM bookings")
myresult = mycursor.fetchall()
list = []
for x in range(len(myresult)):

    room_dict = {}
    room_dict['bookingid'] = myresult[x][0]
    room_dict['roomid'] = myresult[x][1]
    room_dict['start'] = myresult[x][2].strftime("%Y-%m-%d")
    room_dict['end'] = myresult[x][3].strftime("%Y-%m-%d")
    room_dict['duration'] = myresult[x][4]
    room_dict['payment'] = myresult[x][5]
    room_dict['name'] = myresult[x][1]
    if myresult[x][1][0] == "A":
        room_dict['color'] = "red accent-2"
        list.append(room_dict)
        mydb.commit()
    elif myresult[x][1][0] == "B":
        room_dict['color'] = "blue accent-2"
        list.append(room_dict)
        mydb.commit()
    elif myresult[x][1][0] == "C":
        room_dict['color'] = "green accent-2"
        list.append(room_dict)
        mydb.commit()
print list
