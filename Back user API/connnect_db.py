#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lib --------------------------------------------------------------------------
from flask import Flask, request, jsonify, current_app, abort, send_from_directory
from flask_cors import CORS, cross_origin
from functools import wraps
from flaskext.mysql import MySQL
# from flask_mail import Mail, Message
from datetime import timedelta
import base64
import random
import json
import os
import datetime
import string
import requests
import csv
import jwt
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# ------------------------------------------------------------------------------

# connection database ----------------------------------------------------------
app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "1234"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'myusers'

mysql = MySQL()
mysql.init_app(app)

def connect_sql():
    def wrap(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Setup connection
                connection = mysql.connect()
                cursor = connection.cursor()
                return_val = fn(cursor, *args, **kwargs)
            finally:
                # Close connection
                connection.commit()
                connection.close()
            return return_val
        return wrapper
    return wrap
# ------------------------------------------------------------------------------

# connection api ---------------------------------------------------------------
def api_oneid():
    apiOneID = "https://one.th/api"
    return apiOneID
# ------------------------------------------------------------------------------

# format json ------------------------------------------------------------------
def toJson(data,columns):
    results = []
    for row in data:
        results.append(dict(zip(columns, row)))
    return results
# ------------------------------------------------------------------------------

# log server -------------------------------------------------------------------
def logserver(txt):
    current_app.logger.info(txt)
# ------------------------------------------------------------------------------

# decode & encode --------------------------------------------------------------
def decode(data):
    return base64.b64decode(data[:-5][::-1])

def encode(data):
    #[::-1] + id_generator()
    return (base64.b64encode(str(data)))[::-1] + id_generator()

def id_generator():
    size = 5
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
# ------------------------------------------------------------------------------

# http status code (404,405)----------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'fail', "error_message": "Not Found", "result": None}),404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'message': 'fail', "error_message": "Method Not Allowed", "result": None}),405
# ------------------------------------------------------------------------------
