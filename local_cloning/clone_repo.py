from git import Repo #import git library 
import sys #import sys to use command line arguments

#open the command line argument file
input_file = open(sys.argv[1],'r') 

#read the file and split at the newlines, giving a list of all the URLs
urls = input_file.read().splitlines() 

#start a counter for creating cloned repo folder names
counter = 1 

#loops through all of the URLs
for url in urls:

    #clone the current URL into a directory named after the current counter value
    Repo.clone_from(url, "cloned_repos/" + str(counter) + "/") #i.e. first URL will be put in a directory called '1', second URL will be put in '2', etc.
    
    #increment the counter
    counter = counter + 1