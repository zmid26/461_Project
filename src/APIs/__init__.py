
from flask import Flask
import ratepackage, packagebyname, auth, packageid
import mysql.connector

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False # Keeps the JSON output in the same order as the database
app.register_blueprint(ratepackage.bp)
app.register_blueprint(packagebyname.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(packageid.bp)

# Connect to the database
cnx = mysql.connector.connect(
    user='root', password='Pushpop1170', host='localhost', database='461db')


if __name__ == '__main__':
    app.run()