import requests as rq
from pprint import pprint
import sys

def getResponsiveScore(githubRepoURL):

    #githubRepoURL.replace('\n','')

    repoDir = githubRepoURL.split('https://github.com/')[1]

    openURL = 'https://api.github.com/search/issues?q=repo:' + repoDir + '+type:issue+state:open&per_page=1'
    closedURL = 'https://api.github.com/search/issues?q=repo:' + repoDir + '+type:issue+state:closed&per_page=1'

    '''f = open('env.txt', 'r') # open file containing github token
    github_token = f.readline()[13:].replace('\n', '') # retrieve github token
    headers = {'Authorization': 'token ' + github_token} # build the header
    '''

    openResp = (rq.get(url=openURL)).json()
    closedResp = (rq.get(url=closedURL)).json()

    openNum = openResp['total_count']
    closedNum = closedResp['total_count']

    score = max(0,(closedNum - openNum) / closedNum)

    return score

def main():
    testFile = open(sys.argv[1],'r')
    urls = testFile.readlines()

    for u in urls:
        print('Responsive Maintainer score for repo: ', u, ',\nis: ',getResponsiveScore(u))

if __name__ == "__main__":
    main()
