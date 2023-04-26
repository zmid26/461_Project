curl -H "Content-Type: application/json" -d '{
  "metadata": {
    "Name": "string",
    "Version": "1.2.3",
    "ID": "string"
  },
  "data": {
    "Content": "string",
    "URL": "string",
    "JSProgram": "string"
  }
}' -X PUT localhost:5000/package/1