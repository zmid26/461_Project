from pathlib import Path
from collections import Counter
from git import Repo #import git library 
import sys #import sys to use command line arguments
import os

#keep track of which index of the array we are at
url_idx = 0

#list of dictionaries, where each dictionary is 
output = []

#open the command line argument file
input_file = open(sys.argv[1],'r') 

#read the file and split at the newlines, giving a list of all the URLs
urls = input_file.read().splitlines() 

#loops through all of the URLs
for url in urls:
    output.append({"URL":url})


dir = Path('metric_out_files/')

for file in dir.glob('*.txt'):
    with open(file) as metric:
        for line in metric:
            (output[url_idx]).update({"RAMP_UP_SCORE":float(line.strip())})
            url_idx+=1

print(output)
