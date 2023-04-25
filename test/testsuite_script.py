import subprocess
from subprocess import DEVNULL

net_scores = []

# open files containing urls and extract urls
with open('test/good_urls.txt') as good_urls:
    urls = good_urls.readlines() 
with open('test/bad_urls.txt') as bad_urls:
    urls.extend(bad_urls.readlines())

for url in urls:
    # run each individual script for metric calculation
    printed_result = str(subprocess.run(['./run', url], stdout=subprocess.PIPE).stdout)
   
    # extract net_score value from output
    try:
        net_print = printed_result.split('"NET_SCORE":')[1]
        net_score = float(net_print.split(',')[0])
    except:
        net_score = -1

    if net_score <= 1 and net_score >= 0: # if the net_score is valid, add it as a passed test
        net_scores.append(net_score)
        
print("Total: " + str(len(urls)))
print("Passed: " + str(len(net_scores)))
print("Coverage: n/a%")
print("%i/%i test cases passed. n/a%% line coverage achieved" % (len(net_scores), len(urls)))

exit(0)