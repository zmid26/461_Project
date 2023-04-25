
# Function to provide each API file with the database configuration 
from flask import g
import mysql.connector

def db_connect():
    if "cnx" not in g:
        g.cnx = mysql.connector.connect(user='root', password='Cocorello2002!', host='localhost', database='testbed')
    return g.cnx
