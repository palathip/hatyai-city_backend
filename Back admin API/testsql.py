# -*- coding: utf-8 -*- #
from flask import Flask, request, jsonify, current_app, abort, send_from_directory, send_file,Response
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


@app.route('/btest',methods=["GET"])
def gett():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database='test'
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name FROM bbb")
    myresult = mycursor.fetchall()
    data = []
    for x in myresult:
        print(x)
        data.append(x)
        # data = {'name':x}
    # print data/
    return jsonify(data)


##################### API แสดงสถานะห้องว่าง จาก table room ##########################

@app.route('/roomStatus',methods=["GET"])
def gett():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database='bookingsdb')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT room_id,room_type,status FROM rooms")
    myresult = mycursor.fetchall()
    list = []
    for x in range(len(myresult)):
        room_dict = {}
        room_dict['roomid'] = myresult[x][0]
        room_dict['roomtype'] = myresult[x][1]
        room_dict['roomstatus'] = myresult[x][2]
        list.append(room_dict)
    return jsonify(list)

################################################################################

@app.route('/boombibu/<user>/<password>/<role>',methods=['GET'])

def usertest(user,password,role):
    userlist = [{"username": user,"password": password,"role":role},
                {"username": "abc","password": "ccc","role":"user"},
                {"username": "ccc","password": "ccc","role":"user"},
                {"username": "acc","password": "ccc","role":"user"}]
    data = {"result": userlist}
    return jsonify(data)

@app.route('/userpass/<user>/<password>/<role>',methods=['GET'])

#########################  API FORM Bookings TABLES ###############################

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
        room_dict['color'] = "red accent-2"
        list.append(room_dict)
        mydb.commit()
    return jsonify(list)

app.run(host='0.0.0.0',port=3000)

########################################################################################

############################## API อัพเดตการชำระเงิน ########################################

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
########################################################################################

############################ API รับ Booking ID ผ่าน paht ################################

@app.route('/show_booking/<book_id>',methods=["GET"])
def getp(book_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT booking_id,room_id,date_checkin,date_checkout,days_number,payment FROM bookings WHERE booking_id ='%s'"%book_id)
    myresult = mycursor.fetchall()
    list = []
    for x in range(len(myresult)):
        room_dict = {}
        room_dict['booking_id'] = myresult[x][0]
        room_dict['room_id'] = myresult[x][1]
        room_dict['date_checkin'] = myresult[x][2].strftime("%Y-%m-%d")
        room_dict['date_checkout'] = myresult[x][3].strftime("%Y-%m-%d")
        room_dict['day_number'] = myresult[x][4]
        room_dict['payment'] = myresult[x][5]
        list.append(room_dict)
        mydb.commit()
    return jsonify(list)


# DELETE BOOKING โดยรับค่า ID จาก FrontEnd ################################################################################

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

# API ค้นหาห้อง (กิต) #####################################################################################################

@app.route('/search_room', methods=['GET', 'POST'])
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
        input_days_number = request.form["days_number"]



        add_room_all = []
        mysql1 = mydb.cursor()
        mysql1.execute("SELECT rooms.room_id FROM rooms LEFT JOIN (SELECT room_id FROM bookings "
                       "where( bookings.date_checkin BETWEEN '%s' and '%s') and (bookings.date_checkout BETWEEN '%s' and '%s') "
                       "or ( '%s' BETWEEN bookings.date_checkin and bookings.date_checkout) or ( '%s' BETWEEN bookings.date_checkin and bookings.date_checkout)) "
                       "as book ON rooms.room_id = book.room_id where book.room_id is null and rooms.room_type = '%s'"
                       %(input_check_in,input_check_out,input_check_in,input_check_out,input_check_in,input_check_out,input_type.upper()))
        myresult1 = mysql1.fetchall()
        for null_r in myresult1:
            add_room_all.append(null_r)

        d= { "room-id": str(add_room_all), "room_empty":len(add_room_all),"guests_number":input_guests_number,"days_number":input_days_number}
        return jsonify({"Output":d})

#######################################################################################################################