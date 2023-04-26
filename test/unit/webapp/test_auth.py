from webapp import client
import pytest
# from __init__ import login
import mock
from mock import call
from mock import patch
import json

# Mock all database interactions in auth.py
mock_select_user = ('root', 1, 'password1234')

# Function to create schema for testing
def create_schema(username, isAdmin, password):
    schema = {"User": {"name": username, "isAdmin": isAdmin},"Secret": {"password": password}}
    return schema

@mock.patch('src.APIs.auth.select_user', return_value=mock_select_user)
@pytest.mark.parametrize("schema, status_code", [
    (create_schema("root", True, "password1234"), 200),
    # (create_schema("nobody", False, "notapassword"), 404),
    ])
def test_mock_auth(mock_select_user, client, schema, status_code):
    landing = client.put("/authenticate", json=schema)
    html = landing.data.decode()
    assert landing.status_code == status_code
    print(html)
