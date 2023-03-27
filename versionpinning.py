###############################################################
#   Name: Jack Kwan
#   File: versionpinning.py
#   Last modified: 3/25/2023
#   Description: This file takes a given package, searches for 
#   a version, and pins dependencies to that version. From this, it will output a score. 
###############################################################    

import subprocess
import re

def versionpinning(package_name):
    required_version = '{1-9}.{1-9}'
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
            dependency_version = match.group(1)
            if dependency_version.startswith(required_version):
                num_pinned += 1

    # Calculate the score based on the fraction of pinned dependencies
    if len(dependencies) == 0:
        score = 1.0
    else:
        score = num_pinned / len(dependencies)

    return score

package = "numpy"
score = versionpinning(package)

#print(f'The score for {package_name} is {score:.2f}')