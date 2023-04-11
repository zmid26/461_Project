##################################################################################
#   Name: Jack Kwan
#   File: versionpinning.py
#   Last modified: 3/25/2023
#   Description: 
#   This is a Python function that takes in the name of a package as input and 
#   returns a score based on the percentage of its dependencies that are pinned to specific versions. 
#   The function performs the following steps:
#       1. Uses the subprocess module to run a command to get the installed version of the package.
#       2. Extracts the major and minor version numbers from the installed version of the package and writes it to a requirements.txt file.
#       3. Uses another command to get the list of dependencies for the package and extracts their names.
#       4. Loops over the dependencies, using the subprocess module to get the installed version of each dependency.
#       5. Extracts the major and minor version numbers from the installed version of each dependency 
#          and checks if it matches a required version pattern ({1-9}.{1-9}). If it does, it increments a counter of pinned dependencies.
#       6. Calculates a score based on the fraction of pinned dependencies out of the total number of dependencies.
#       7. Returns the score.
##################################################################################    

import subprocess
import re
import sys

def versionpinning(package_name):
    #required_version = '{1-9}.{1-9}'
    # Get the installed version of the package
    cmd = f'pip show {package_name}'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode()
    match = re.search(r'Version: (\d+\.\d+)', output)
    if match:
        installed_version = match.group(1)
    else:
        print(f'Error: Could not determine installed version of {package_name}')
        exit(1)

    # Pin the package to the major and minor version
    version_pin = f'{package_name}=={installed_version.split(".")[0]}.{installed_version.split(".")[1]}'

    # Write the version pin to a requirements.txt file
    with open('requirements.txt', 'w') as file:
        file.write(version_pin)

    # Get the list of dependencies for the package
    cmd = f'pip show --no-cache-dir --no-color {package_name} | grep Requires'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode()

    # Split the output into lines and extract the package names
    dependencies = []
    for line in output.splitlines():
        matches = re.findall(r'[^\s]+', line)
        dependencies.extend(matches[1:])

    # Pin the dependencies to the required version and count the number of pinned dependencies
    num_pinned = 0
    for dependency in dependencies:
        cmd = f'pip show {dependency}'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        output = result.stdout.decode()
        match = re.search(r'Version: (\d+\.\d+)', output)
        if match:
            num_pinned += 1

    # Calculate the score based on the fraction of pinned dependencies
    if len(dependencies) == 0:
        score = 1.0
    else:
        score = num_pinned / len(dependencies)

    return score

def main():
    version_pinning_score = versionpinning(sys.argv[1])
    with open('output/versionpining.txt', 'w') as f:
        f.write(str(version_pinning_score))
        f.write('\n')
        f.close()
if __name__ == "__main__":
    main()