import requests
import sys # import sys to use command line arguments
import json # import json to parse json file
import os
import logging
from verbosity import setup_logging

devnull = open('/dev/null', 'w')
sys.stdout = devnull
sys.stderr = devnull

# Setup logging
setup_logging()

# Get github_token from environment variables
github_token = os.environ.get('GITHUB_TOKEN')

with open(sys.argv[1],'r') as f: # open file containing urls
  urls = f.readlines() 

repositories = []
for x in range(len(urls)): # extract owner and name of each repository

  repoName = urls[x].partition('github.com/')[2] # extract "owner/repo"

  if not repoName: # if github.com/ is not found, extract as npmjs package
    with open('output/cloned_repos/' + str(x+1) + '/package.json') as json_File:
      npmsRepo = json.load(json_File) # load json file containing repo debug
    repoName = npmsRepo['repository'] # extract repo debug

    if not isinstance(repoName, str): # if a dict is returned instead of str
      repoName = list(repoName.values())[1] # extract url from dict
      repoName = repoName.partition('github.com/')[2].replace('.git','') # extract "owner/repo"
  
  repositories.append((repoName.partition('/')[0],repoName.partition('/')[2].replace('\n',''))) # append (owner, repo)

url = 'https://api.github.com/graphql' # graphql url
headers = {'Authorization': 'token ' + github_token} # build the header

# run requests
with open('output/correctness_out.txt', 'w') as f:
  for repository in repositories:
    logging.debug('current analysis of correctness will be done with github GraphQL api')
    logging.debug('beginning retrieval of information from repository %s %s' % (repository[0],repository[1]))

    # build the query to retrieve needed debug using from the given repo
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
      logging.debug('successful graphQL api retrieval with code %d' % response.status_code)

      try:
        starCount = response.json()["data"]["repository"]["stargazerCount"]
        openIssuesCount = response.json()["data"]["repository"]["openIssues"]["totalCount"]
        correctness = starCount / (starCount + openIssuesCount * 10) # calculate correctness
        
        logging.debug('proper repo format - data retrieval successful')
        logging.info('Repo had %d stars' % starCount)
        logging.info("Correctness score for repo ")#%s owned by %s: %f" % (repository[1], repository[0], correctness))

      except:
        logging.debug('improper repo format - error with repo')
        print('error with repo')

      #write the correctness score to the outputfile
      f.write(str(correctness))
      f.write('\n')
    
    else: # handle error if response is not received correctly
      logging.debug('Failed to retrieve response with code %d' % response.status_code)
