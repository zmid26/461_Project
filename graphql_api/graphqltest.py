import requests

api_token = "insert_token"

url = 'https://api.github.com/graphql'
json = { 'query' : '{ viewer { repositories(first: 30) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)
print (r.text)