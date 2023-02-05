import requests

f = open('env.txt', 'r') # open file containing github token
github_token = f.readline()[13:].replace('\n', '') # retrieve github token
f2 = open('url_file.txt', 'r') # open file containing urls
urls = f2.readlines() 
repositories = []
for url in urls: # extract owner and name of each repository
  repositories.append((url.partition('github.com/')[2].partition('/')[0],url.partition('github.com/')[2].partition('/')[2].replace('\n','')))

url = 'https://api.github.com/graphql' # graphql url
headers = {'Authorization': 'token ' + github_token} # build the header

# run requests
for repository in repositories:
  # build the query to retrieve needed info using from the given repo
  query = '''
  query {
    repository(owner: "%s", name: "%s") {
      stargazerCount
      openIssues: issues(states: OPEN) {
        totalCount
      }
    }
  }
  ''' % (repository[0], repository[1])
  json = { 'query' : query }

  response = requests.post(url=url, json=json, headers=headers)
  if response.status_code == 200: # extract the result from the response
    starCount = response.json()["data"]["repository"]["stargazerCount"]
    openIssuesCount = response.json()["data"]["repository"]["openIssues"]["totalCount"]
    correctness = starCount / (starCount + openIssuesCount) # calculate correctness
    print("Correctness score for repo %s owned by %s: %f" % (repository[1], repository[0], correctness))
  else: # handle error if response is not received correctly
    raise Exception("Failed to retrieve response using GraphQL by returning code {}. {}".format(response.status_code, query))