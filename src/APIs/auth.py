from flask import request, jsonify
import datetime
import jwt
import jsonschema
from jsonschema import validate
from flask.blueprints import Blueprint
from database import db_connect

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
            cur = cnx.cursor()
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
            
            return token #should not be error , what can I write for it to not show up in the response?

        except jsonschema.exceptions.ValidationError as err:
            return jsonify({"error": "There is missing field(s) in the AuthenticationRequest or it is formed improperly."}), 400
    else:
        return jsonify({"error": "This system does not support authentication."}), 501

# Function to interact with database
def select_user(username, isAdmin, password, cur):
    query = ("SELECT * FROM User WHERE name = %s AND isAdmin = %s AND password = %s")
    cur.execute(query, (username, isAdmin, password))
    result = cur.fetchone()
    return result