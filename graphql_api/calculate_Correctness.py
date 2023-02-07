import requests
import sys # import sys to use command line arguments
import json # import json to parse json file

f = open('env.txt', 'r') # open file containing github token
github_token = f.readline()[13:].replace('\n', '') # retrieve github token
f.close()
f2 = open(sys.argv[1],'r') # open file containing urls
urls = f2.readlines() 
f2.close()

repositories = []
for x in range(len(urls)): # extract owner and name of each repository
  repoName = urls[x].partition('github.com/')[2] # extract "owner/repo"

  if not repoName: # if github.com/ is not found, extract as npmjs package
    with open('local_cloning/cloned_repos/' + str(x+1) + '/package.json') as json_File:
      npmsRepo = json.load(json_File) # load json file containing repo info
    repoName = npmsRepo['repository'] # extract repo info

    if not isinstance(repoName, str): # if a dict is returned instead of str
      repoName = list(repoName.values())[1] # extract url from dict
      repoName = repoName.partition('github.com/')[2].replace('.git','') # extract "owner/repo"
  
  repositories.append((repoName.partition('/')[0],repoName.partition('/')[2].replace('\n',''))) # append (owner, repo)

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
    correctness = starCount / (starCount + openIssuesCount * 10) # calculate correctness
    print("Number of stars: %i" % starCount)
    print("Number of open issues: %i" % openIssuesCount)
    print("Correctness score for repo %s owned by %s: %f \n" % (repository[1], repository[0], correctness))
  
  else: # handle error if response is not received correctly
    print("Failed to retrieve response using GraphQL by returning code {}.".format(response.status_code))