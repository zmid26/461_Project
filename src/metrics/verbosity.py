import os
import sys
import logging

#function to set up logging
def setup_logging():
    devnull = open('/dev/null', 'w')
    sys.stdout = devnull
    sys.stderr = devnull

    # Get log_file and log_level from environment variables
    log_fstr = os.environ.get('LOG_FILE')
    logLvl = os.environ.get('LOG_LEVEL')

    #baed on logLvl, set log level to INFO if 0, DEBUG if 1, ERROR if 2
    if logLvl == '0':
        logLvl = logging.INFO
    elif logLvl == '1':
        logLvl = logging.DEBUG
    elif logLvl == '2':
        logLvl = logging.ERROR
    else:
        logLvl = logging.INFO
        
    #format for logging = logging.<level>(`<message>`)
    logging.basicConfig(filename=log_fstr, level=logLvl, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('logging level set to %s' % logLvl)
