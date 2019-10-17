# -*- coding: utf-8 -*-
import mysql
from flask import Flask, redirect, jsonify, current_app, abort, send_from_directory, send_file, Response, request
from sqlalchemy.dialects.mysql import pymysql
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='')

# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
# app.config['MYSQL_DATABASE_DB'] = 'auto'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#
#
# # @app.route('/selectuser', methods=['GET'])
# def user():
#     mycursor = mydb.cursor()
#     mycursor.execute("SELECT firstname FROM myusers")
#     data_group = cursor.fetchall()
#     # columns_group = [column[0] for column in cursor.description]
#     # # return toJson(data_group,columns_group)
#     print "dd $s"%data_group



# app.run(host='localhost', port='5000')



import json
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="192.168.74.159", #192.168.74.159
  user="root",
  passwd="",
  database='bookingsdb' #bookingsdb
)

@app.route('/search_room', methods=['GET', 'POST'])
@cross_origin()
def select():
    if request.method == 'GET':
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM rooms")
        myresult = mycursor.fetchall()
        add=[]
        for index in range(len(myresult)):
            list_user = {"room_id": myresult[index][0], "room_type": myresult[index][1], "price": myresult[index][3]}
            add.append(list_user)
        return jsonify({"result":add})

    elif request.method == 'POST':
        data = request.json
        input_check_in = request.form["check_in"]
        input_check_out = request.form["check_out"]
        input_type = str(request.form["type"])

        input_guests_number = request.form["guests_number"]
        # input_days_number = request.form["days_number"]
        # input_rooms_number = str(request.form["rooms_number"])
        # input_days_number = input_check_out
        temp1 = datetime.datetime.strptime(input_check_in,"%Y-%m-%d")
        temp2 = datetime.datetime.strptime(input_check_out, "%Y-%m-%d")
        x=temp2-temp1
        # print x.days

        add_room_all = []
        mysql1 = mydb.cursor()
        mysql1.execute("SELECT rooms.room_id FROM rooms LEFT JOIN (SELECT room_id FROM bookings "
                       "where( bookings.date_checkin BETWEEN '%s' and '%s') and (bookings.date_checkout BETWEEN '%s' and '%s') "
                       "or ( '%s' BETWEEN bookings.date_checkin and bookings.date_checkout) or ( '%s' BETWEEN bookings.date_checkin and bookings.date_checkout)) "
                       "as book ON rooms.room_id = book.room_id where book.room_id is null and rooms.room_type = '%s'"
                       %(input_check_in, input_check_out,input_check_in,input_check_out,input_check_in,input_check_out,input_type.upper()))
        myresult1 = mysql1.fetchall()
        for null_r in myresult1:
            add_room_all.append(null_r)

        d= { "room-id": str(add_room_all), "room_empty":len(add_room_all),"guests_number":int(input_guests_number),"days_number":x.days}
        return jsonify({"Output":d})



@app.route('/booking', methods=['POST'])
@cross_origin()
def insert_data():
    data = request.json
    input_date_checkin = request.form["date_checkin"]
    input_date_checkout = request.form["date_checkout"]
    input_room_id = str(request.form["room_id"])
    input_firstname = request.form["firstname"]
    input_lastname = request.form["lastname"]
    input_email = request.form["email"]
    input_phone = request.form["phone"]
    input_guests_number = request.form["guests_number"]
    input_days_number = request.form["days_number"]
    # input_rooms_number = request.form["rooms_number"]
    input_booking_price = request.form["booking_price"]
    input_select_payment = request.form["select_payment"]

    if input_select_payment == "option1":
        select_pay = 1
    if input_select_payment == "option2":
        select_pay = 0
    # // k_bug --------------
    # xx = input_room_id.replace("[(u'", '').replace("')", '')
    # xx1 = xx.replace("',), (u", '')
    sql_insert = mydb.cursor()
    sql_in = "INSERT INTO bookings (room_id, firstname, lastname, email, phone, date_checkin, date_checkout, guests_number, days_number, booking_price, payment) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)"
    val = (input_room_id[4:7], input_firstname, input_lastname, input_email, input_phone, input_date_checkin, input_date_checkout, input_guests_number, input_days_number, input_booking_price, select_pay)
    sql_insert.execute(sql_in,val)
    mydb.commit()

    mycursor_se = mydb.cursor()
    mycursor_se.execute("SELECT booking_id FROM bookings ORDER BY create_timestamp DESC LIMIT 1")
    myresult_se = mycursor_se.fetchall()
    booking_id1 = str(myresult_se).replace("[(","")
    booking_id2 =booking_id1.replace(",)]","")
    return jsonify({"booking_id":booking_id2})

@app.route('/update', methods=['PUT'])
def update_data():
    data = request.json
    input_room_id = request.form["room_id_upd"]
    input_firstname = request.form["firstname_upd"]
    input_lastname = request.form["lastname_upd"]

    sql_update = mydb.cursor()
    sql_up = "UPDATE bookings SET firstname = %s, lastname = %s WHERE booking_id = %s "
    val_up = (input_firstname, input_lastname, input_room_id)
    sql_update.execute(sql_up,val_up)
    mydb.commit()
    return jsonify("Update success!",val_up)

app.run(host='0.0.0.0', port='5000')
mydb.close()