from flask import request, jsonify, make_response, Response
import datetime
import jwt
import jsonschema
from jsonschema import validate
from flask.blueprints import Blueprint
from .database import db_connect
from functools import wraps

bp = Blueprint('auth', __name__)

input_schema = {
  "type": "object",
  "properties": {
    "User": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "isAdmin": {
          "type": "boolean"
        }
      },
      "required": ["name", "isAdmin"]
    },
    "Secret": {
      "type": "object",
      "properties": {
        "password": {
          "type": "string"
        }
      },
      "required": ["password"]
    }
  },
  "required": ["User", "Secret"]
}

def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Authorization')
        if not token:
            return make_response('', 400)

        try:
            payload = jwt.decode(token, 'dyhgccydyxrtxttrxtrzxrt', algorithms=['HS256'])
            # add the payload to the request object for future use in the function
            request.payload = payload
        except jwt.InvalidTokenError:
            return make_response('', 400)

        return func(*args, **kwargs)

    return wrapper

@bp.route('/authenticate', methods=['PUT'])
def generate_token():
    cnx = db_connect()
    if request.is_json:
        try:
            validate(request.json, input_schema)
            username = request.json["User"]["name"]
            isAdmin = request.json["User"]["isAdmin"]
            password = request.json["Secret"]["password"]

            cnx.reconnect()
            cur = cnx.cursor(buffered = True)
            result = select_user(username, isAdmin, password, cur)
            cnx.commit()
            cur.close()
            cnx.close()

            if not result:
                return make_response('', 401)
           
            payload = {
            'sub': username
            }
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=10)

            # Generate the JWT token
            token = jwt.encode(
                {
                'exp': expiration_time,
                'iat': datetime.datetime.utcnow(),
                'payload': payload
                },
            'dyhgccydyxrtxttrxtrzxrt',
            algorithm='HS256'
            )
            
            #response = Response()
            #response.headers['X-Authorization'] = token
            #response.set_cookie('X-Authorization', token)
            return token

            #return token #should not be error , what can I write for it to not show up in the response?

        except jsonschema.exceptions.ValidationError as err:
            return make_response('', 400)
    else:
        return make_response('', 501)


# helpful function for knowing flask app is up
@bp.route('/')
def hello():
    return "Hello there"

# helpfful function for knowing the react app can access the flask app
@bp.route("/andrew")
def andrew():
    return jsonify({"message": "flask app connected"})

# Function to interact with database
def select_user(username, isAdmin, password, cur):
    query = ("SELECT * FROM User WHERE name = %s AND isAdmin = %s AND password = %s")
    cur.execute(query, (username, isAdmin, password))
    result = cur.fetchone()
    return result