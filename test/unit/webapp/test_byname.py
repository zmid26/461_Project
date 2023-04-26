from webapp import client
import pytest
# from __init__ import login
import mock
from mock import call
from mock import patch

# Log client in
# def test_login(client):
#     response = login(client, flask.app.config['USERNAME'], flask.app.config['PASSWORD'])
#     # get authentification token and store it in flask.app.config['TOKEN']

# List of packages and their expected status codes (200 if package exists, 404 if package does not exist)
@pytest.mark.parametrize("name, status_code", [
    ("Cloudinary", 200),
    ("Invalid", 200),
    ("Package", 404),
    ("DNE", 404)
])
def test_byname_get(client, name, status_code):
    landing = client.get(f"/package/byname/{name}")
    assert landing.status_code == status_code
    #html = landing.data.decode()
    #print(f"\n{html}\n")

# Mock all database interactions in get_package_by_name
mock_version = (1000)
mock_user_data = ("root", 1)
mock_package_entry_history = [(100, "root", "Thu, 06 Apr 2023 00:00:00 GMT", "CREATE")]
mock_ids = [(100,), (101,), (102,), (103,)]

@mock.patch('src.APIs.packagebyname.get_ids', return_value=mock_ids)
@mock.patch('src.APIs.packagebyname.get_package_entry', return_value=mock_package_entry_history)
@mock.patch('src.APIs.packagebyname.get_ids', return_value=mock_user_data)
@mock.patch('src.APIs.packagebyname.get_version', return_value=mock_version)
@pytest.mark.parametrize("name, status_code", [
    ("Cloudinary", 200),
    ("Invalid", 200),
    ("Package", 200),
    # ("DNE", 404)
])

def test_mock_byname_get(version, user_data, package_entry_history, ids, client, name, status_code):
    landing = client.get(f"/package/byname/{name}")
    html = landing.data.decode()
    assert landing.status_code == status_code
    assert "[", "]" in html
    print(html)

# Mock all database interactions in delete_package_by_name
@mock.patch('src.APIs.packagebyname.delete_from_PackageRating')
@mock.patch('src.APIs.packagebyname.delete_from_PackageEntryHistory')
@mock.patch('src.APIs.packagebyname.delete_from_Package')
@pytest.mark.parametrize("name, status_code", [
    ("Cloudinary", 200),
    ("Invalid", 200),
    ("Package", 404),
    ("DNE", 404)
])

def test_mock_byname_delete(package, entryhistory, rating, client, name, status_code):
    landing = client.delete(f"/package/byname/{name}")
    assert landing.status_code == status_code
    html = landing.data.decode()
    print(html)
