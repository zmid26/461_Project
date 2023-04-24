from flask import Flask, request, jsonify
import json
import jsonschema
from jsonschema import validate
import mysql.connector

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

cnx = mysql.connector.connect(user='root', password='Cocorello2002!', host='localhost', database='testBed')

idvalue = 0

input_schema = {
  "type": "object",
  "properties": {
    "Content": {
      "type": "string"
    },
    "URL": {
      "type": "string",
      "format": "uri"
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


@app.route('/package', methods=['POST'])
def package():
    global idvalue
    idvalue += 1
    # Expect JSON input
    if request.is_json:
        try:
            validate(request.json, input_schema)
            
            name = request.json["Content"]
            content = request.json["Content"]
            url = request.json["URL"]
            jsprog = request.json["JSProgram"]
            cnx.reconnect()
            cur = cnx.cursor()

            insert_query = "INSERT INTO Package (ID, Name, Version, Content, URL, JSProgram) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (idvalue, name, 2.0, 'fsddf', url, jsprog)
            cur.execute(insert_query, values)

            cnx.commit()
            cur.close()
            cnx.close()

            metadata = {
            "Name": name,
            "Version": "1.0.0",
            "ID": idvalue
            }
            data = {
            "Content": content,
            "JSProgram": jsprog
            }
            response = {"metadata": metadata, "data": data}
            return jsonify(response)

        except jsonschema.exceptions.ValidationError as err:
            return jsonify({"error": "There is missing field(s) in the PackageID/AuthenticationToken or it is formed improperly, or the AuthenticationToken is invalid."}), 400
    else:
        return jsonify({"error": "Package is not uploaded due to the disqualified rating."}), 424


@app.route('/package/<int:id>', methods=['GET'])
def get_package(id):

  cnx.reconnect()
  cur = cnx.cursor()
  cur.execute("SELECT * FROM Package WHERE ID = %s", (id,))
  package = cur.fetchone()
  cnx.commit()
  cur.close()
  cnx.close()

  if package is None:
    return jsonify({'error': 'Package does not exist.'}), 404
  
  metadata = {
    "Name": package[1],
    "Version": package[2],
    "ID": package[0]
  }
  data = {
    "URL": package[4],
    "JSProgram": package[5]
  }
  response = {"metadata": metadata, "data": data}
  return jsonify(response)

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

@app.route('/package/<int:id>', methods=['PUT'])
def put_package(id):
  if request.is_json:
    try:
      validate(request.json, input_schema2)
  
      #check if package exists 
      cnx.reconnect()
      cur = cnx.cursor()
      cur.execute("SELECT * FROM Package WHERE ID = %s", (id,))
      package = cur.fetchone()
      cnx.commit()
      cur.close()
      cnx.close()

      if package is None:
        return jsonify({'error': 'Package does not exist.'}), 404
      
      #get input data 
      metadata = request.json["metadata"]
      name = metadata["Name"]
      version = metadata["Version"]
      metadata = request.json["data"]
      content = metadata["Content"]
      url = metadata["URL"]
      jsprogram = metadata["JSProgram"]

      #update
      cnx.reconnect()
      cur = cnx.cursor()
      cur.execute("UPDATE Package SET Name = %s, Version = %s, Content = %s, URL = %s, JSProgram = %s WHERE ID = %s",(name, version, content, url, jsprogram, id))
      cnx.commit()
      cur.close()
      cnx.close()

      return jsonify({"type": "Version is updated."})
    except jsonschema.exceptions.ValidationError as err:
      return jsonify({"error": "There is missing field(s) in the PackageID/AuthenticationToken or it is formed improperly, or the AuthenticationToken is invalid."}), 400
  else:
        return jsonify({"error": "NEEDS TO BE REPLACED OR DESTROYED"}), 424


@app.route('/package/<int:id>', methods=['DELETE'])
def delete_package(id):

  cnx.reconnect()
  cur = cnx.cursor()
  cur.execute("SELECT * FROM Package WHERE ID = %s", (id,))
  package = cur.fetchone()
  cnx.commit()
  cur.close()
  cnx.close()
  if package is None:
    return jsonify({'error': 'Package does not exist.'}), 404
  
  cnx.reconnect()
  cur = cnx.cursor()
  cur.execute("DELETE FROM Package WHERE ID = %s", (id,))
  cnx.commit()
  cur.close()
  cnx.close()
  return jsonify({"message": "Package is deleted."}), 200


if __name__ == '__main__':
    app.run()