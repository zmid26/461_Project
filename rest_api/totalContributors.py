from github import Github
import urllib.request as url
import re
import sys
import os

def getGithubURLs(repo):
    webUrl = url.urlopen(repo)
    if(webUrl.getcode() == 200):
        html_cont = webUrl.read().decode("utf-8")
        r1 = r'<span id="repository-link">(.*?)<\/span>'
        try:
            reg_out = re.search(r1, html_cont)
            gitLink = ("https://" + reg_out.group(1))
        except:
            raise Exception("Valid GitHub link not found.\n")
    else:
        raise Exception("npm url not able to connect.\n")
    return gitLink

def main():
    givenUrl = sys.argv[1]

    if "npmjs.com/" in givenUrl:
        gitURL = getGithubURLs(givenUrl)
    else:
        gitURL = givenUrl

    github_token = os.environ.get('GITHUB_TOKEN')
    try:
        token = Github(github_token)
        repo = token.get_repo(gitURL.split("github.com/", 1)[1])       #Obtain the repo from rest API
        numContributors = repo.get_contributors(anon="true")        #Get the list of contributors using PyGithub
        print(f"{numContributors.totalCount}")                           #Return the total count of contributors
    except:
        print("0")

if __name__ == "__main__":
    main();
