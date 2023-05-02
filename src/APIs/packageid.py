from flask import request, jsonify, make_response
import json
import jsonschema
from jsonschema import validate
import base64
import io
import zipfile
import os
from flask.blueprints import Blueprint
from .database import db_connect
from .auth import *
import requests
import logging


bp = Blueprint('packageid', __name__)

idvalue = 0

input_schema = {
  "type": "object",
  "properties": {
    "Content": {
      "type": "string"
    },
    "JSProgram": {
      "type": "string"
    },
    "URL": {
      "type": "string"
    }
  },
  "required": [
    "JSProgram"
  ]
}


#TESTING
base64_string = "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"
#logging.basicConfig(filename='app.log', level=logging.DEBUG)
@bp.route('/package', methods=['POST'], endpoint='postEND')
#@token_required
def package():
    # Connect to database
    cnx = db_connect()
    print(f"PATH (POST): {request.path} \n")
    print(f"REQUEST BODY: {request.json} \n")
  
    global idvalue
    idvalue += 1
    # Expect JSON input
    if request.is_json:
        try:
            validate(request.json, input_schema)
            
            if "Content" in request.json:
            #if "Content" in request.json:
              content = request.json["Content"]
              jsprog = request.json["JSProgram"]
              
            
            # BELOW
              zip_file_bytes = base64.b64decode(content)
              zip_file_io = io.BytesIO(zip_file_bytes)

              with zipfile.ZipFile(zip_file_io, 'r') as zip_file:
                fileList = zip_file.namelist()
                for index, file_path in enumerate(fileList):
                  if 'package.json' in file_path:
                    package_json_bytes = zip_file.read(fileList[index])
                    package_json_str = package_json_bytes.decode('utf-8')
                    data = json.loads(package_json_str)
                    name = data['name']
                    version = data['version']
                    url = data['repository']['url']
                  else:
                    zero = 0
            #ABOVE

            if "URL" in request.json:
              jsprog = request.json["JSProgram"]
              url = request.json["URL"]
              owner, repo = url.split('/')[-2:]
              response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/zipball")
              content = base64.b64encode(response.content).decode('utf-8')
              package_response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contents/package.json")

              # Parse the package.json file to extract the name and version of the package
              package_info = json.loads(base64.b64decode(package_response.json()['content']).decode('utf-8'))
              name = package_info['name']
              version = package_info['version']

            #https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#download-a-repository-archive-zip
            '''
            cnx.reconnect()
            cur = cnx.cursor()
            insert_query = "INSERT INTO Package (ID, Name, Version, Content, JSProgram) VALUES (%s, %s, %s, %s, %s)"
            values = (idvalue, name, version, content, jsprog)
            cur.execute(insert_query, values)

            cnx.commit()
            cur.close()
            cnx.close()
            '''
            search_stmt = sqlalchemy.text("SELECT * FROM Package WHERE Name=:name AND Version = :version")
            package = cnx.execute(search_stmt, parameters={"name": name, "version": version}).fetchone()
            cnx.commit()

            if package:
              return make_response('', 409)

            insert_stmt = sqlalchemy.text("INSERT INTO Package (ID, Name, Version, Content, JSProgram, URL) VALUES (:idvalue, :name, :version, :content, :jsprog, :url)")
            cnx.execute(insert_stmt, parameters={"idvalue": idvalue, "name": name, "version": version, "content": content, "jsprog": jsprog, "url": url})
            cnx.commit()


            metadata = {
            "Name": name,
            "Version": version,
            "ID": idvalue
            }
            data = {
            "Content": content,
            "JSProgram": jsprog
            }
            response = {"metadata": metadata, "data": data}
            print(f"RESPONSE BODY: {response}")
            return jsonify(response), 201 
            
        except jsonschema.exceptions.ValidationError as err:
            #print("schema error")
            return make_response('', 400)
    else:
        return make_response('', 424)

# Function to interact with database
def post_package(content, jsprog, cur, name, version, url):
    insert_query = "INSERT INTO Package (ID, Name, Version, Content, JSProgram, URL) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (idvalue, name, version, content, jsprog, url)
    cur.execute(insert_query, values)


@bp.route('/package/<int:id>', methods=['GET'], endpoint = 'getEND')
#@token_required
def get_package(id):
  # Connect to database
  #bp.logger.info('Request body: %s', request.get_data())
  #bp.logger.info('Request headers: %s', request.headers)
  cnx = db_connect()
  print(f"PATH: {request.path} \n")
  print(f"REQUEST BODY: {request.json} \n")

  ####### DO ANOTHER MERGE 
  # Get package from the database
  #package = get_package(id, cnx)
  search_stmt = sqlalchemy.text("SELECT * FROM Package WHERE ID=:id")
  package = cnx.execute(search_stmt, parameters={"id": id}).fetchone()
  cnx.commit()

  if package is None:
    return make_response('', 404)
  
  metadata = {
    "Name": package[1],
    "Version": package[2],
    "ID": package[0]
  }
  data = {
    "Content": package[3],
    "JSProgram": package[5]
  }
  response = {"metadata": metadata, "data": data}

  #bp.logger.info(f"Request: {request.method} {request.url} Headers: {request.headers} Body: {request.json}")
  #bp.logger.info(f"Response: {response}")
  print(f"RESPONSE BODY: {response}")
  return jsonify(response)

# Function to interact with database
def get_package(id, cnx):

    search_stmt = sqlalchemy.text("SELECT * FROM Package WHERE ID=:id")
    package = cnx.execute(search_stmt, parameters={"id": id}).fetchone()
    cnx.commit()

    '''
    cnx.reconnect()
    cur = cnx.cursor(buffered = True)
    cur.execute("SELECT * FROM Package WHERE ID = %s", (id,))
    package = cur.fetchone()
    cnx.commit()
    cur.close()
    cnx.close()
    '''
    # print(package)
    return package

input_schema2 = {
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "Name": {
          "type": "string"
        },
        "Version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        },
        "ID": {
          "type": "string"
        }
      },
      "required": [
        "Name",
        "Version",
        "ID"
      ]
    },
    "data": {
      "type": "object",
      "properties": {
        "Content": {
          "type": "string"
        },
        "URL": {
          "type": "string"
        },
        "JSProgram": {
          "type": "string"
        }
      },
      "required": [
        "Content",
        "URL",
        "JSProgram"
      ]
    }
  },
  "required": [
    "metadata",
    "data"
  ]
}

@bp.route('/package/<int:id>', methods=['PUT'], endpoint = 'putEND')
#@token_required
def put_package(id):
  # Connect to database
  cnx = db_connect()

  if request.is_json:
    try:
      validate(request.json, input_schema2)
  
      #check if package exists 
      package = get_package(id, cnx)

      if package is None:
        return make_response('', 404)
      
      #get input data 
      metadata = request.json["metadata"]
      name = metadata["Name"]
      version = metadata["Version"]
      metadata = request.json["data"]
      content = metadata["Content"]
      url = metadata["URL"]
      jsprogram = metadata["JSProgram"]

      #update
      update_package(id, cnx, name, version, content, url, jsprogram)

      return make_response('', 200)
    except jsonschema.exceptions.ValidationError as err:
      return make_response('', 400)
  else:
        return make_response('', 424)

def update_package(id, cnx, name, version, content, url, jsprogram):

    search_stmt = sqlalchemy.text("UPDATE Package SET Name =:name, Version =:version, Content =:content, URL =:url, JSProgram =:jsprogram WHERE ID =:id")
    cnx.execute(search_stmt, parameters={"name": name, "version": version, "content": content, "url": url, "jsprogram": jsprogram, "id": id})
    cnx.commit()
    '''
    cnx.reconnect()
    cur = cnx.cursor(buffered=True)
    cur.execute("UPDATE Package SET Name = %s, Version = %s, Content = %s, URL = %s, JSProgram = %s WHERE ID = %s",(name, version, content, url, jsprogram, id))
    cnx.commit()
    cur.close()
    cnx.close()
    '''

@bp.route('/package/<int:id>', methods=['DELETE'], endpoint = 'deleteEND')
#@token_required
def delete_package(id):
  # Connect to database
  cnx = db_connect()

  # Get package from the database
  package = get_package(id, cnx)

  if package is None:
    return make_response('', 404)
  
  delete_from_db(id, cnx)
  return make_response('', 200)

# Function to interact with database
def delete_from_db(id, cnx):
    search_stmt = sqlalchemy.text("DELETE FROM Package WHERE ID =:id")
    cnx.execute(search_stmt, parameters={"id": id})
    cnx.commit()
    '''
    cnx.reconnect()
    cur = cnx.cursor()
    cur.execute("DELETE FROM Package WHERE ID = %s", (id,))
    cnx.commit()
    cur.close()
    cnx.close()
    '''


@bp.route('/reset', methods=['DELETE'], endpoint = 'resetEND')
#@token_required
def reset_package():
  cnx = db_connect()

  search_stmt = sqlalchemy.text("DELETE FROM Package")
  cnx.execute(search_stmt)
  cnx.commit()
  '''
  cnx.reconnect()
  cur = cnx.cursor()
  cur.execute("DELETE FROM Package")
  cnx.commit()
  cur.close()
  cnx.close()
  '''
  return make_response('', 200)

