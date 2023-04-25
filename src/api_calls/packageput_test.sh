curl -H "Content-Type: application/json" -d '{
  "metadata": {
    "Name": "Package",
    "Version": "1.2.3",
    "ID": "100"
  },
  "data": {
    "Content": "string",
    "URL": "string",
    "JSProgram": "string"
  }
}' -X PUT localhost:5000/package