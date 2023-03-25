from github import Github
import urllib.request as url
import re
import sys

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

    env_file = open('.env')
    vars = env_file.readlines()
    for v in vars:
        if v.find("GITHUB_TOKEN") != -1:
            github_token = v.split("GITHUB_TOKEN=")[1]
            github_token = github_token.replace('\n','')

    try:
        token = Github(github_token)
        repo = token.get_repo(gitURL.split("github.com/", 1)[1])
        statsContributors = repo.get_stats_contributors()
        numCommits = 0
        for contributor in statsContributors:
            numCommits += contributor.total
        print(f"{numCommits}")
    except:
        print("0")

if __name__ == "__main__":
    main()
