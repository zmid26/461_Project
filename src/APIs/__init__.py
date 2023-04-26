from flask import Flask
from . import ratepackage, packagebyname, auth, packageid
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
app.json.sort_keys = False  # Keeps the JSON output in the same order as the database
app.register_blueprint(ratepackage.bp)
app.register_blueprint(packagebyname.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(packageid.bp)
CORS(app)

# Connect to the database
cnx = mysql.connector.connect(
    user='root', password='Pushpop1170', host='localhost', database='461db')


if __name__ == '__main__':
    app.run()