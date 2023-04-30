# Function to provide each API file with the database configuration 
from flask import g
# import mysql.connector

# def db_connect():
#     if "cnx" not in g:
#         g.cnx = mysql.connector.connect(user='root', password='Cocorello2002!', host='34.29.104.3', database='461db')

#     return g.cnx

from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    # initialize Connector object
    connector = Connector()
    conn: pymysql.connections.Connection = connector.connect(
        "ece461-project:us-central1:instancemysql",
        "pymysql",
        user="root",
        password="Cocorello2002!",
        db="461db"
    )
    return conn

def db_connect():
    if "cnx" not in g:
        # create connection pool
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
        )
        g.cnx = pool.connect()
    return g.cnx