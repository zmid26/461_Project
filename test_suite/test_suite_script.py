import subprocess
from subprocess import DEVNULL

net_scores = []

# open files containing urls and extract urls
with open('test_suite/good_urls.txt') as good_urls:
    urls = good_urls.readlines() 
with open('test_suite/bad_urls.txt') as bad_urls:
    urls.extend(bad_urls.readlines())

for url in urls:
    # create a new file for each url
    with open("test_suite/newTest.txt", "w") as newTestFile:
        newTestFile.write(url.strip())

    # run each individual script for metric calculation
    printed_result = str(subprocess.run(['./run', 'test_suite/newTest.txt'], stdout=subprocess.PIPE).stdout)
   
    # extract net_score value from output
    try:
        net_print = printed_result.split('"NET_SCORE":')[1]
        net_score = float(net_print.split(',')[0])
    except:
        net_score = -1

    if net_score <= 1 and net_score >= 0: # if the net_score is valid, add it as a passed test
        net_scores.append(net_score)

    '''
    # wip coverage score
    # run each individual script to find coverage
    #rust_coverage = subprocess.run(['./target/debug/calculate_ramp_up', 'test_suite/newTest.txt'], shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=DEVNULL).stdout
    subprocess.run(['python3 -m coverage run --source=. graphql_api/calculate_Correctness.py test_suite/newTest.txt'],shell=True, executable='/bin/bash', stdout=DEVNULL, stderr=DEVNULL)
    subprocess.run(['python3 -m coverage run -a --source=. rest_api/calculate_ResponsiveMaintainer.py test_suite/newTest.txt'], shell=True, executable='/bin/bash', stdout=DEVNULL, stderr=DEVNULL)
    subprocess.run(['python3 -m coverage run -a --source=. local_cloning/license.py test_suite/newTest.txt'], shell=True, executable='/bin/bash', stdout=DEVNULL, stderr=DEVNULL)
    subprocess.run(['python3 -m coverage run -a --source=. output/print_results.py test_suite/newTest.txt'], shell=True, executable='/bin/bash', stdout=DEVNULL, stderr=DEVNULL)
    subprocess.run(['python3 -m coverage run -a --source=. verbosity.py test_suite/newTest.txt'], shell=True, executable='/bin/bash', stdout=DEVNULL, stderr=DEVNULL)
    python_coverage = subprocess.run(['python3 -m coverage report'], shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=DEVNULL)
    python_coverage = str(python_coverage.stdout)
    print(python_coverage)
    with open("test_suite/coverage.txt", "w") as newTestFile:
        newTestFile.write(python_coverage)

    # extract coverage percents
    python_coverage_score = python_coverage[(python_coverage.find('TOTAL') + 61):63]
    print(python_coverage_score)
    #rust_coverage_score = rust_coverage.find(')

    # 28.75% code is rust, 71.25% is python
    #total_coverage_score = 0.2875 * rust_coverage_score + 0.7125 * rust_coverage_score
    '''
        
print("Total: " + str(len(urls)))
print("Passed: " + str(len(net_scores)))
#print("Coverage: " + str(total_coverage_score*100) + "%")
print("%i/%i test cases passed." % (len(net_scores), len(urls)))

exit(0)