import os #import subproccess to run CLI commands in the code
import sys

devnull = open('/dev/null', 'w')
sys.stderr = devnull

if not os.system("pip3 install GitPython"): #install gitpython
    os.system("pip3 install GitPython") #install gitpython with pip3

<<<<<<< HEAD
if not os.system("pip3 install PyGithub"): #install PyGithub
    os.system("pip3 install PyGithub")
=======
if not os.system("pip3 install requests"): #install gitpython
    os.system("pip3 install requests") #install gitpython with pip3
>>>>>>> 16e6740d0d1d944b3a9de755787cebc3ca4d4894

os.system("cargo update -p ignore --precise 0.4.18")

exit(0) #exit 0 on success
