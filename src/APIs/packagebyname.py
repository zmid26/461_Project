'''
This file contains the following api calls:
    - /package/byname/<string:Name> (GET)
    - /package/byname/<string:Name> (DELETE)

    **Until authentication token is provided, both calls will return a 400**
'''
from flask import Flask, request, abort
import mysql.connector

app = Flask(__name__)
# Keeps the JSON output in the same order as the database
app.config['JSON_SORT_KEYS'] = False

# Connect to the database
cnx = mysql.connector.connect(
    user='root', password='Pushpop1170', host='localhost', database='461db')


# Returns all packages with name = Name from the database
@app.route('/package/byname/<string:Name>', methods=['GET'])
def get_package_by_name(Name):
    # TODO: If header information is incorrect or auth token is invalid, return a 400
    # As is this will return a 400 as no token is provided
    # token = request.headers.get('X-Authorization')
    # if token is None:
    #     abort(400)

    # Get all ids with name = Name
    cursor = cnx.cursor()
    query = "SELECT ID FROM Package WHERE Name = %s"
    cursor.execute(query, (Name,))
    ids = cursor.fetchall()
    print("got id with name = Name")

    # If the package doesn't exist, return a 404
    if len(ids) == 0:
        print("package does not exist, returning 404")
        cursor.close()
        abort(404)

    # For each id, get the package entry history from PackageEntryHistory
    package_entry_history = []
    packageshistory = []
    query = "SELECT * FROM PackageEntryHistory WHERE ID = %s"
    for id in ids:
        id = id[0]
        cursor.execute(query, (id,))
        package_entry_history.append(cursor.fetchall())

        # Get user data for each package entry
        for i in range(len(package_entry_history[-1])):
            query = "SELECT name, isAdmin FROM User WHERE name = %s"
            cursor.execute(query, (package_entry_history[-1][i][1],))
            userdata = cursor.fetchall()

            query = "SELECT Version FROM Package WHERE ID = %s"
            cursor.execute(query, (package_entry_history[-1][i][0],))
            version = cursor.fetchone()

            # Combine the user data with the package entry history in correct format
            user = {"name": userdata[0][0], "isAdmin": userdata[0][1]}
            metadata = {"Name": Name, "Version": version,
                        "ID": package_entry_history[-1][i][0]}

            packagehistory = {"User": user, "Date": package_entry_history[-1][i][2],
                              "PackageMetadata": metadata, "Action": package_entry_history[-1][i][3]}
            packageshistory.append(packagehistory)

    return ((packageshistory))


# Deletes all instances of a packages with name = Name from the database
@app.route('/package/byname/<string:Name>', methods=['DELETE'])
def delete_package_by_name(Name):
    # TODO: If header information is incorrect or auth token is invalid, return 400
    # As is this will return a 400 as no token is provided
    token = request.headers.get('X-Authorization')
    if token is None:
        abort(400)

    cursor = cnx.cursor()

    # Get all ids with name = Name
    query = "SELECT ID FROM Package WHERE Name = %s"
    cursor.execute(query, (Name,))
    ids = cursor.fetchall()

    # If the package doesn't exist, return a 404
    if len(ids) == 0:
        print("package does not exist, returning 404")
        cursor.close()
        abort(404)

    # Delete all instances where id = id from PackageRating
    for id in ids:
        id = id[0]
        print(id)
        print("Deleting id = {} from PackageRating".format(id))
        query = "DELETE FROM PackageRating WHERE ID = %s"
        cursor.execute(query, (id,))

        # Delete all instances where id = id from PackageEntryHistory
        print("Deleting id = {} from PackageEntryHistory".format(id))
        query = "DELETE FROM PackageEntryHistory WHERE ID = %s"
        cursor.execute(query, (id,))

        cnx.commit()

    # Delete all instances where name = Name from Package
    print("delete from Package where Name = %s", Name)
    query = "DELETE FROM Package WHERE Name = %s"
    cursor.execute(query, (Name,))
    cnx.commit()
    cursor.close()
    return '', 200


# Run the app
if __name__ == "__main__":
    app.run()
