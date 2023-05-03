import os
import subprocess

print(subprocess.check_output("./run https://github.com/jashkenas/underscore", env=os.environ, shell=True))
