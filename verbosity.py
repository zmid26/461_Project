import os
import sys

devnull = open('/dev/null', 'w')
sys.stdout = devnull
sys.stderr = devnull

env_file = open('.env')
vars = env_file.readlines()


log_fstr = os.getenv('LOG_FILE')
log_fstr = str(log_fstr)

logLvl = os.getenv('LOG_LEVEL')
logLvl = int(logLvl)



if logLvl == 1:
    logTemp = open('log/logv1.txt','r')
    logInfo = logTemp.readlines()
elif logLvl == 2:
    logTemp = open('log/logv2.txt','r')
    logInfo = logTemp.readlines()
else:
    logInfo = []
  
try:
    log_true = open(log_fstr,'w+')
except:
    log_true = open('log_file.txt','w+')


for t in logInfo:
    log_true.write(t)
    