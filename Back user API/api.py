
from flask import Flask, redirect, jsonify, current_app, abort, send_from_directory, send_file, Response, request

app = Flask(__name__, static_url_path='')

# CORS(app)
# app.config['MYSQL_DATABASE_USER'] = ""
# app.config['MYSQL_DATABASE_PASSWORD'] = ""
# app.config['MYSQL_DATABASE_DB'] = ""
# app.config['MYSQL_DATABASE_HOST'] = ""



# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Expose-Headers', 'X-Token')
#     response.headers.add('Access-Control Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTION')
#     return response


@app.route('/test', methods=['GET'])
def test():
    print ("test")
    return jsonify({'A': "test"})

@app.route('/login', methods=['POST'])
def login():
    input_jason = request.json
    user = input_jason['username']
    password = input_jason['password']

    if user == 'aaaa' and password =='bbbb':
        return jsonify({'result' : 'Login success'})
    else:
        return jsonify({'result': 'Login error'})


@app.route('/user/<user>/<password>/<role>', methods=['GET'])
def user1(user,password,role):
    list_user =[{"username": user, "password": password, "role": role}]
    data = {
        "result":list_user
    }
    return jsonify(data)


app.run(host='localhost', port='5000')