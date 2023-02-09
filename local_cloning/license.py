import re
import os
from pathlib import Path

readme_pattern = re.compile("(?i)README.md")
license_pattern = re.compile("(?i)license")
found = 0

rootdir = 'local_cloning/cloned_repos/'
with open('output/license_out.txt', 'w') as f:
  for file in os.listdir(rootdir):
      d = os.path.join(rootdir, file)
      if os.path.isdir(d):
        found = 0
        for root, dirs, files in os.walk(d):
          for x in files:
            if readme_pattern.match(x) and found == 0:
              valid_readme_file = os.path.join(root,x)
              with open(valid_readme_file, 'r') as readme:
                text = readme.read()
                if('license' or 'LICENSE' or 'License' in text):
                  f.write(str(1.0))
                  f.write('\n')
                else:
                  f.write(str(0.0))
                  f.write('\n')
                found = 1

            
            