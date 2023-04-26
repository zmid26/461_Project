import pytest
from src.APIs.__init__ import app

# Create client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['USERNAME'] = 'admin'    # Replace username/password with valid credentials (?)
    app.config['PASSWORD'] = 'admin'
    app.config['TOKEN'] = None

    client = app.test_client()
    yield client

# # Log in client (currently with username and password as admin)
# @pytest.fixture
# def login(client, username, password):
#     return client.put('/authenticate', data=dict(
#         username= username,
#         password= password
#     ), follow_redirects=True)