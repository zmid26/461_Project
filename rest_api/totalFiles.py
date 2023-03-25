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
        repo = token.get_repo(gitURL.split("github.com/", 1)[1])    #Obtain the repo from rest API 
        contents = repo.get_contents("")                            #Get all files contained in the repo
        numFiles = []                                               #List that will contain all file objects
        #Parse through all file objects created by PyGithub
        while contents:                             
            files_content = contents.pop(0)                         #Pop out the top file
            if(files_content.type == "dir"):                            #If the file is a directory, recursively get the subdirectory file objects
                contents.extend(repo.get_contents(files_content.path))
            else:
                numFiles.append(files_content)                      #Add the specific file object to the list
        print(f"{len(numFiles)}")                                        #Return the length of the list
    except:
        print("0")

if __name__ == "__main__":
    main()
