import os

env_file = open('.env')
vars = env_file.readlines()

for v in vars:
    if v.find('LOG_FILE') != -1:
        log_fstr = v.split('LOG_FILE=')[1]
        log_fstr = log_fstr.replace('\n','')
    if v.find('LOG_LEVEL') != -1:
        logLvl = v.split('LOG_LEVEL=')[1]
        logLvl = logLvl.replace('\n','')
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
    