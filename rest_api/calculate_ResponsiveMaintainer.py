import requests as rq
from pprint import pprint
import sys
import json

def getResponsiveScore(githubRepoURL):

    repoDir = githubRepoURL.split('https://github.com/')[1]

    # format each github url for the REST api
    # we want to get the number of open and closed issues in the repo

    openURL = 'https://api.github.com/search/issues?q=repo:' + repoDir + '+type:issue+state:open&per_page=1'
    closedURL = 'https://api.github.com/search/issues?q=repo:' + repoDir + '+type:issue+state:closed&per_page=1'

    f = open('env.txt', 'r') # open file containing github token
    github_token = f.readline()[13:].replace('\n', '') # retrieve github token
    headers = {'Authorization': 'token ' + github_token} # build the header for authentication
   
   # get a response using the REST API
    openResp = (rq.get(url=openURL,headers=headers))
    closedResp = (rq.get(url=closedURL,headers=headers))

    # if the response is successful, get the issue numbers
    if openResp.status_code == 200 and closedResp.status_code == 200:
        
        # test if the repos contain the correct data in json format
        try:
            openNum = openResp.json()['total_count']
            closedNum = closedResp.json()['total_count']
        except:
            print('improper repo format- investigate repo at ',githubRepoURL)
            return -1

        # calculate ration of open to closed requests for score
        score = max(0,(closedNum - openNum) / closedNum)

        return score
    
    # return invalid score if not able to get repo information
    else:
        print('failed to resolve repository: ',githubRepoURL,' as ',openURL)

        return -1


def getGithubURLs(repos):
  
    repositories = []
    for x in range(len(repos)): # extract owner and name of each repository
        repoName = repos[x].partition('github.com/')[2] # extract "owner/repo"

        if not repoName: # if github.com/ is not found, extract as npmjs package
            with open('local_cloning/cloned_repos/' + str(x+1) + '/package.json') as json_File:
                npmsRepo = json.load(json_File) # load json file containing repo info
                repoName = npmsRepo['repository'] # extract repo info

            if not isinstance(repoName, str): # if a dict is returned instead of str
                repoName = list(repoName.values())[1] # extract url from dict
                repoName = repoName.partition('github.com/')[2].replace('.git','') # extract "owner/repo"
    
        repositories.append((repoName.partition('/')[0],repoName.partition('/')[2].replace('\n',''))) # append (owner, repo)

    #convert all repos to github urls
    gitLinks = []

    for r in repositories:
        currLink = 'https://github.com/' + r[0] + '/' + r[1]
        gitLinks.append(currLink)

    #return list of github urls
    return gitLinks

def main():

    #read in data from test file
    testFile = open(sys.argv[1],'r')
    urls = testFile.readlines()

    #clear newlines from all urls
    for u in range(len(urls)):
        urls[u] = urls[u].replace('\n','')

    #convert any npm repos to github
    gitURLs = getGithubURLs(urls)

    #find and print the responsive maintainer metric for each repo
    for u in gitURLs:
        print('\nResponsive Maintainer score for repo: ', u, '\nis: ',getResponsiveScore(u),'\n')

if __name__ == "__main__":
    main()
