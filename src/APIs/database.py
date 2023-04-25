
# Function to provide each API file with the database configuration 
from flask import g
import mysql.connector

def db_connect():
    if "cnx" not in g:
        g.cnx = mysql.connector.connect(user='root', password='Pushpop1170', host='localhost', database='461db')
    return g.cnx
