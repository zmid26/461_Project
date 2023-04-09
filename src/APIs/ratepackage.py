'''
This file contains the following api call:
    - /package/<int:id>/rate (GET)

    **Assumes server is started from project_461 directory**
    **Until authentication token is provided, this will return a 400**

'''

from flask import Flask, request, jsonify, abort
import mysql.connector
import subprocess
import json
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False # Keeps the JSON output in the same order as the database

# Connect to the database
cnx = mysql.connector.connect(
    user='root', password='password123', host='localhost', database='461db')

# Rates a package if it exists and stores the rating in the database
@app.route('/package/<int:id>/rate', methods=['GET'])
def rate_package(id):
    # TODO: If header information is incorrect or auth token is invalid, return a 400
    # ****As is code will return a 400 as no token is provided***
    token = request.headers.get('X-Authorization')
    if token is None:
        abort(400)
        
    # Get the package url from the database
    cursor = cnx.cursor()
    query = "SELECT URL FROM Package where ID= %s"
    cursor.execute(query, (id,))
    package_url = cursor.fetchone()
    cursor.close()

    # If the package doesn't exist, return a 404
    if package_url is None:
        return "Package {} not found".format(id), 404
    else:
        package_url = package_url[0]

    # Set the relative path to the CLI from the directory the server was started from **update this**
    # Currently assumes the server is started from the project_461 directory
    clipath = "./run"

    # ./run "package_url" from and return the results
    rating = subprocess.check_output(
        "{} {}".format(clipath, package_url), shell=True)
    
    # If the rating returns an error, return a 500
    result = rating.decode("utf-8")
    if len(result) < 174:
        return "Error: Could not get rating for package {} with error = {}".format(id,result), 500
    rating = json.loads(rating)

    # Insert the results into the database
    # See if ID is already in PackageRating
    cursor = cnx.cursor()
    query = "SELECT * FROM PackageRating WHERE ID = %s"
    cursor.execute(query, (id,))
    package_rating = cursor.fetchone()

    if package_rating is None:
        # Insert the rating into the database
        print("Inserting rating into database")
        query = "INSERT INTO PackageRating (ID, BusFactor, Correctness, RampUp, ResponsiveMaintainer, LicenseScore, GoodPinningPractice, PullRequest, NetScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (id, rating["BusFactor"], rating["Correctness"], rating["RampUp"], rating["ResponsiveMaintainer"],
                       rating["LicenseScore"], rating["GoodPinningPractice"], rating["PullRequest"], rating["NetScore"]))
        
        # Add time package was rated in PackageEntryHistory
        print("Marking id = {} as deleted in PackageEntryHistory".format(id))
        query = "INSERT INTO PackageEntryHistory (ID, Username, Date, Action) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id, "placeholder", datetime.now(), "RATE"))
    else:
        # Update the rating in the database
        print("Updating rating in database")
        query = "UPDATE PackageRating SET BusFactor = %s, Correctness = %s, RampUp = %s, ResponsiveMaintainer = %s, LicenseScore = %s, GoodPinningPractice = %s, PullRequest = %s, NetScore = %s WHERE ID = %s"
        cursor.execute(query, (rating["BusFactor"], rating["Correctness"], rating["RampUp"], rating["ResponsiveMaintainer"],
                       rating["LicenseScore"], rating["GoodPinningPractice"], rating["PullRequest"], rating["NetScore"], id))
        
        # Add time package was updated in PackageEntryHistory
        print("Marking id = {} as deleted in PackageEntryHistory".format(id))
        query = "INSERT INTO PackageEntryHistory (ID, Username, Date, Action) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id, "placeholder", datetime.now(), "UPDATE"))

    cnx.commit()
    cursor.close()

    return jsonify(rating)


if __name__ == '__main__':
    app.run()
