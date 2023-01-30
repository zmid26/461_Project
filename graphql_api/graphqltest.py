import requests

api_token = "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"
#api_token = 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

url = 'https://api.github.com/graphql'
json = { 'query' : '{ viewer { repositories(first: 30) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)
print (r.text)