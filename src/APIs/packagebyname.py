'''
This file contains the following api calls:
    - /package/byname/<string:Name> (GET)
    - /package/byname/<string:Name> (DELETE)

    **Until authentication token is provided, both calls will return a 400**
'''
from flask import abort
from flask.blueprints import Blueprint
from .database import db_connect

bp = Blueprint('packagebyname', __name__)

# Returns all packages with name = Name from the database
@bp.route('/package/byname/<string:Name>', methods=['GET'])
def get_package_by_name(Name):
    cnx = db_connect()

    # TODO: If header information is incorrect or auth token is invalid, return a 400
    # As is this will return a 400 as no token is provided
    # token = request.headers.get('Authorization')
    # if token is None:
    #     abort(400)

    # Get all ids with name = Name
    cursor = cnx.cursor()
    ids = get_ids(Name, cursor)
    
    # If the package doesn't exist, return a 404
    if len(ids) == 0:
        print("package does not exist, returning 404")
        cursor.close()
        abort(404)

    # For each id, get the package entry history from PackageEntryHistory
    package_entry_history = []
    packageshistory = []
    for id in ids:
        id = id[0]
        package_entry_history.append(get_package_entry(cursor, id))
        # print(package_entry_history)
        # Get user data for each package entry
        for i in range(len(package_entry_history[-1])):
            userdata = get_user_data(cursor, package_entry_history, i)
            version = get_version(cursor, package_entry_history, i)

            # Combine the user data with the package entry history in correct format
            user = {"name": userdata[0][0], "isAdmin": userdata[0][1]}
            metadata = {"Name": Name, "Version": version,
                        "ID": package_entry_history[-1][i][0]}

            packagehistory = {"User": user, "Date": package_entry_history[-1][i][2],
                              "PackageMetadata": metadata, "Action": package_entry_history[-1][i][3]}
            packageshistory.append(packagehistory)

    return ((packageshistory))

# Functions used to interact with the database
def get_version(cursor, package_entry_history, i):
    query = "SELECT Version FROM Package WHERE ID = %s"
    cursor.execute(query, (package_entry_history[-1][i][0],))
    version = cursor.fetchone()
    # print(f"version is {version}")
    return version

def get_user_data(cursor, package_entry_history, i):
    query = "SELECT name, isAdmin FROM User WHERE name = %s"
    cursor.execute(query, (package_entry_history[-1][i][1],))
    userdata = cursor.fetchall()
    return userdata

def get_package_entry(cursor, id):
    query = "SELECT * FROM PackageEntryHistory WHERE ID = %s"
    cursor.execute(query, (id,))
    return cursor.fetchall()

def get_ids(Name, cursor):
    query = "SELECT ID FROM Package WHERE Name = %s"
    cursor.execute(query, (Name,))
    ids = cursor.fetchall()
    # print(f"got id with name = {Name}")
    return ids


# Deletes all instances of a packages with name = Name from the database
# Deletes entries in PackageEntryHistory, Package, PackageRating
@bp.route('/package/byname/<string:Name>', methods=['DELETE'])
def delete_package_by_name(Name):
    cnx = db_connect()

    # TODO: If header information is incorrect or auth token is invalid, return 400
    # As is this will return a 400 as no token is provided
    # token = request.headers.get('X-Authorization')
    # if token is None:
    #     abort(400)

    cursor = cnx.cursor()

    # Get all ids with name = Name
    ids = get_ids(Name, cursor)

    # If the package doesn't exist, return a 404
    if len(ids) == 0:
        print("package does not exist, returning 404")
        cursor.close()
        abort(404)

    # Delete all instances where id = id from PackageRating
    for id in ids:
        id = id[0]
        print(id)
        delete_from_PackageRating(cursor, id)

        # Delete all instances where id = id from PackageEntryHistory
        print("Deleting id = {} from PackageEntryHistory".format(id))
        delete_from_PackageEntryHistory(cursor, id)

    # Delete all instances where name = Name from Package
    print("delete from Package where Name = %s", Name)
    delete_from_Package(Name, cursor)
    cnx.commit()
    cursor.close()
    return '', 200

# Functions used to interact with the database
def delete_from_Package(Name, cursor):
    query = "DELETE FROM Package WHERE Name = %s"
    cursor.execute(query, (Name,))

def delete_from_PackageEntryHistory(cursor, id):
    query = "DELETE FROM PackageEntryHistory WHERE ID = %s"
    cursor.execute(query, (id,))

def delete_from_PackageRating(cursor, id):
    print("Deleting id = {} from PackageRating".format(id))
    query = "DELETE FROM PackageRating WHERE ID = %s"
    cursor.execute(query, (id,))
