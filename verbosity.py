import os

logLvl = os.environ.get('LOG_LEVEL')

if logLvl == '2':
    logTemp = open('log/logv2.txt','r')
    logInfo = logTemp.readlines()
elif logLvl == '3':
    logTemp = open('log/logv3.txt','r')
    logInfo = logTemp.readlines()
else:
    logInfo = []

log_true = open('log_file.txt','w+')

for t in logInfo:
    log_true.write(t)
    