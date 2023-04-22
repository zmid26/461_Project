curl -H "Content-Type: application/json" -d '{
  "User": {
    "name": "root",
    "isAdmin": true
  },
  "Secret": {
    "password": "password1234"
  }
}' -X PUT localhost:5000/authenticate -v