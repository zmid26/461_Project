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
'''
# Define a custom decorator to require the JWT token in the request header
def jwt_required(func):
    def wrapper(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Extract the JWT token from the request header
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Authorization token is missing'}), 401

        try:
            # Decode and verify the JWT token
            data = jwt.decode(token, 'secret_key_here', algorithms=['HS256'])
            current_user = data['payload']
        except:
            return jsonify({'message': 'Invalid token'}), 401

        # Attach the decoded user data to the request object and execute the endpoint function
        return func(current_user, *args, **kwargs)
    return wrapper

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Authorization' in request.headers:
            token = request.headers['X-Authorization']
        if not token:
            return jsonify({'error': 'Token is missing.'}), 401

        try:
            data = jwt.decode(token, 'X-Authorization', algorithms=['HS256'])
            current_user = data['username']
        except jwt.exceptions.DecodeError:
            return jsonify({'error': 'Invalid token.'}), 401

        return func(current_user, *args, **kwargs)

    return decorated
'''

def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Authorization')
        if not token:
            return jsonify({"error": "Token is missing."}), 401

        try:
            payload = jwt.decode(token, 'X-Authorization', algorithms=['HS256'])
            # add the payload to the request object for future use in the function
            request.payload = payload
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token is invalid."}), 401

        return func(*args, **kwargs)

    return wrapper


@bp.route('/authenticate', methods=['PUT'])
def generate_token():
    cnx = db_connect()
    if request.is_json:
        try:
            print(type(request.json))
            print(request.json)
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
                return jsonify({"error": "The user or password is invalid."}), 401
           
            payload = {
            'sub': username
            }
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

            # Generate the JWT token
            token = jwt.encode(
                {
                'exp': expiration_time,
                'iat': datetime.datetime.utcnow(),
                'payload': payload
                },
            'X-Authorization',
            algorithm='HS256'
            )
            
            response = Response()
            response.headers['X-Authorization'] = token
            response.set_cookie('X-Authorization', token)
            print(token)
            return response

            #return token #should not be error , what can I write for it to not show up in the response?

        except jsonschema.exceptions.ValidationError as err:
            return jsonify({"error": "There is missing field(s) in the AuthenticationRequest or it is formed improperly."}), 400
    else:
        return jsonify({"error": "This system does not support authentication."}), 501

@bp.route('/protected')
@token_required
def protected_route():
    # Get the payload from the request object
    payload = request.payload

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