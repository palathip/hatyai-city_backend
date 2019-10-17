# -*- coding: utf-8 -*- #
from flask import Flask, request, jsonify
import mysql.connector
import datetime
app = Flask(__name__,static_url_path='')
mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database='bookingsdb')
if (mydb):
    print 'connect success'
else:
    print 'Error'

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Expose-Headers','X-Token')
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response

# API แสดงการจองทั้งหมด ###################################################################################################

@app.route('/show_booking',methods=["GET"])
def gett():
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
        elif myresult[x][1][0] == "B":
            room_dict['color'] = "blue accent-2"
        elif myresult[x][1][0] == "C":
            room_dict['color'] = "green accent-2"
        list.append(room_dict)
        mydb.commit()
    return jsonify(list)

#######################################################################################################################

# API อัพเดตการชำระเงิน #####################################################################################################

@app.route('/payment',methods=["POST"])
def upp():
    books_id = int(request.form["booking_id"]) # ส่วนการรับค่าที่ได้มา
    mycursor = mydb.cursor()
    mycursor.execute("SELECT create_timestamp FROM bookings WHERE booking_id = '%d'"%books_id)
    myresult = mycursor.fetchall()
    now_time = datetime.datetime.now()
    print now_time
    for x in range(len(myresult)):
        print myresult[x][0]
    delta = now_time - myresult[x][0]
    diftime = delta.seconds / 60
    if diftime <= 30:
        mycursor.execute("UPDATE bookings SET payment = 1 WHERE booking_id = '%d'"%books_id)
        mydb.commit()
        return jsonify("Payment Success")
    else:
        mycursor.execute("UPDATE bookings SET payment = 2 WHERE booking_id = '%d'" % books_id)
        mydb.commit()
        return jsonify("Time Out")

#######################################################################################################################

# API ลบการจองโดยรับค่า ID โดย Path จาก FrontEnd ############################################################################

@app.route('/delete_booking/<book_id>',methods=["DELETE"])
def dell(book_id):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM bookings WHERE booking_id ='%s'"%book_id)
    mydb.commit()
    return jsonify("Delete Success")

#######################################################################################################################

app.run(host='0.0.0.0',port=3000)

mycursor.close()
mydb.close()
