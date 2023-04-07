from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/first')
def my_python_function():
    # Define your Python function here
    result = 42
    return jsonify(result=result)

app.run(host='localhost', port=8080)