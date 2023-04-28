'''
This file contains the following api call:
    - /package/<int:id>/rate (GET)

    **Assumes server is started from project_461 directory**
    **Until authentication token is provided, this will return a 400**

'''

from flask import jsonify
import subprocess
import json
from datetime import datetime 
from flask.blueprints import Blueprint
from .database import db_connect 
from .auth import *

bp = Blueprint('ratepackage', __name__)

# Rates a package if it exists and stores the rating in PackageRating table
@bp.route('/package/<int:id>/rate', methods=['GET'])
@token_required
def rate_package(id):
    cnx = db_connect()

    # TODO: If header information is incorrect or auth token is invalid, return a 400
    # ****As is code will return a 400 as no token is provided***
    # token = request.headers.get('X-Authorization')
    # if token is None:
    #     abort(400)
        
    # Get the package url from the database
    package_url = get_package_url(id, cnx)
    #print(package_url)

    # If the package doesn't exist, return a 404
    if package_url is None:
        print("package does not exist, returning 404")
        return "Package {} not found".format(id), 404
    else:
        package_url = package_url[0]

    # Set the relative path to the CLI from the directory the server was started from **update this**
    # Currently assumes the server is started from the project_461 directory
    clipath = "./run"

    # ./run "package_url" from and return the results
    rating = run_cli(package_url, clipath)
    print(rating)
    print(type(rating))
    # If the rating returns an error, return a 500
    result = rating.decode("utf-8")
    if len(result) < 174:
        return "Error: Could not get rating for package {} with error = {}".format(id,result), 500
    rating = json.loads(rating)

    # Insert the results into the database
    # See if ID is already in PackageRating
    cursor = cnx.cursor()
    package_rating = get_package_rating(id, cursor)

    if package_rating is None:
        # Insert the rating into the database
        print("Inserting rating into database")
        insert_rating(id, rating, cursor)
        
        # Add time package was rated in PackageEntryHistory
        print(f"Marking package with id = {id} as rated in PackageEntryHistory")
        mark_as_rated(id, cursor)
    else:
        # Update the rating in the database
        print("Updating rating in database")
        update_rating(id, rating, cursor)
        
        # Add time package was updated in PackageEntryHistory
        print("Marking id = {} as updated in PackageEntryHistory".format(id))
        mark_as_updated(id, cursor)

    cnx.commit()
    cursor.close()

    return jsonify(rating)

# Functions to interact with the database
def mark_as_updated(id, cursor):
    query = "INSERT INTO PackageEntryHistory (ID, Username, Date, Action) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (id, "placeholder", datetime.now(), "UPDATE"))

def update_rating(id, rating, cursor):
    query = "UPDATE PackageRating SET BusFactor = %s, Correctness = %s, RampUp = %s, ResponsiveMaintainer = %s, LicenseScore = %s, GoodPinningPractice = %s, PullRequest = %s, NetScore = %s WHERE ID = %s"
    cursor.execute(query, (rating["BusFactor"], rating["Correctness"], rating["RampUp"], rating["ResponsiveMaintainer"],
                       rating["LicenseScore"], rating["GoodPinningPractice"], rating["PullRequest"], rating["NetScore"], id))

def mark_as_rated(id, cursor):
    query = "INSERT INTO PackageEntryHistory (ID, Username, Date, Action) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (id, "placeholder", datetime.now(), "RATE"))

def insert_rating(id, rating, cursor):
    query = "INSERT INTO PackageRating (ID, BusFactor, Correctness, RampUp, ResponsiveMaintainer, LicenseScore, GoodPinningPractice, PullRequest, NetScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (id, rating["BusFactor"], rating["Correctness"], rating["RampUp"], rating["ResponsiveMaintainer"],
                       rating["LicenseScore"], rating["GoodPinningPractice"], rating["PullRequest"], rating["NetScore"]))

def get_package_rating(id, cursor):
    query = "SELECT * FROM PackageRating WHERE ID = %s"
    cursor.execute(query, (id,))
    package_rating = cursor.fetchone()
    # print(f"package rating = {package_rating}")
    return package_rating

def run_cli(package_url, clipath):
    rating = subprocess.check_output(
        "{} {}".format(clipath, package_url), shell=True)
    
    return rating

def get_package_url(id, cnx):
    cursor = cnx.cursor()
    query = "SELECT URL FROM Package where ID= %s"
    cursor.execute(query, (id,))
    package_url = cursor.fetchone()
    cursor.close()
    return package_url