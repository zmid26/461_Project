import subprocess
from subprocess import DEVNULL

passedTests = 0
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
        passedTests += 1
        net_scores.append(net_score)

    # wip coverage score
    '''
    # run each individual script to find coverage
    #rust_coverage = subprocess.run(['./target/debug/calculate_ramp_up', 'test_suite/newTest.txt'], stdout=subprocess.PIPE).stdout
    subprocess.run(['python3', '-m', 'coverage', 'run', 'graphql_api/calculate_Correctness.py', 'test_suite/newTest.txt'])
    subprocess.run(['python3', '-m', 'coverage', 'run', '-a', 'rest_api/calculate_ResponsiveMaintainer.py', 'test_suite/newTest.txt'])
    subprocess.run(['python3', '-m', 'coverage', 'run', '-a', 'local_cloning/license.py', 'test_suite/newTest.txt'])
    subprocess.run(['python3', '-m', 'coverage', 'run', '-a', 'output/print_results.py', 'test_suite/newTest.txt'])
    python_coverage = subprocess.run(['python3', '-m', 'coverage', 'report'], stdout=subprocess.PIPE)
    print(python_coverage)
    # extract coverage percents
    python_coverage_score = str(python_coverage).find('TOTAL')
    print(python_coverage_score)
    #rust_coverage_score = rust_coverage.find(')

    # 28.75% code is rust, 71.25% is python
    #total_coverage_score = 0.2875 * rust_coverage_score + 0.7125 * rust_coverage_score
    '''
        

print("%i/%i test cases passed." % (passedTests, len(urls)))
print(net_scores)

exit(0)