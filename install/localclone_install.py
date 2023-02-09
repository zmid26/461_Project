import os #import subproccess to run CLI commands in the code


if not os.system("pip3 install GitPython"): #install gitpython
    os.system("pip3 install GitPython") #install gitpython with pip3

os.system("cargo update -p ignore --precise 0.4.18")