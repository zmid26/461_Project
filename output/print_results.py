from pathlib import Path
from collections import Counter
from git import Repo #import git library 
import sys #import sys to use command line arguments
import os
import json

devnull = open('/dev/null', 'w')
sys.stderr = devnull

#keep track of which index of the array we are at
url_idx = 0

#list of dictionaries, where each dictionary is 
output = []
rampup = []
correctness = []
responsive_maintainer = []
netscore = []
license = []

#open the command line argument file
input_file = open(sys.argv[1],'r')

#read the file and split at the newlines, giving a list of all the URLs
urls = input_file.read().splitlines() 

#set the directory with the metric output files
output_file_locations = Path('metric_out_files/')

#open rampup output and add to rampup list
with open("output/rampup_out.txt") as ramp_out:
    for line in ramp_out:
        rampup.append(float(line.strip()))

#open correctness output and add to correctness list
with open("output/correctness_out.txt") as correct_out:
    for line in correct_out:
        correctness.append(float(line.strip()))

#open resp maintain output and add to resp maintain list
with open("output/resp_maintain_out.txt") as resp_out:
    for line in resp_out:
        responsive_maintainer.append(float(line.strip()))

#open license output and add to license list
with open("output/license_out.txt") as lic_out:
    for line in lic_out:
        license.append(float(line.strip()))

#calculate netscore for each url (just chose correctness as iterator because lazy..couldve been any iterator that goes for the number of urls)
url_idx = 0
for x in correctness:
    netscore.append( ((responsive_maintainer[url_idx] * 4.0) + (correctness[url_idx] * 3.0) + (rampup[url_idx] * 2.0) + (license[url_idx])) / 10.0)
    
    url_idx += 1

url_idx = 0

#loop through all the netscores and put the appropriate metrics in the appropriate dictionaries
for x in netscore:
    output.append({})
    (output[url_idx]).update({"URL":urls[url_idx]})
    (output[url_idx]).update({"NET_SCORE":netscore[url_idx]})
    (output[url_idx]).update({"RAMP_UP_SCORE":rampup[url_idx]})
    (output[url_idx]).update({"CORRECTNESS_SCORE":correctness[url_idx]})
    (output[url_idx]).update({"BUS_FACTOR_SCORE":-1})
    (output[url_idx]).update({"RESPONSIVE_MAINTAINER_SCORE":responsive_maintainer[url_idx]})
    (output[url_idx]).update({"LICENSE_SCORE":license[url_idx]})
    url_idx += 1

#sort netscore list and do the same ops to output so that output is sorted in the same way
net_and_out = list(zip(netscore, output))
net_and_out_sorted = sorted(net_and_out, reverse=True)
sorted_output = [x[1] for x in net_and_out_sorted]

#print the sorted output
for x in sorted_output:
    print(json.dumps(x))

exit(0)
