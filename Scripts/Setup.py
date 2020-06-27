""" This is the Starting Point of Kijiji Web Scraping Script """

import sys
import os
import logging
from datetime import datetime
from SetupEnvironment import SetupEnvironment

""" Setting Basic Logging Options """

if not os.path.exists('../Logs') :
    os.makedirs('../Logs')

LOG_FILENAME = datetime.now().strftime('../Logs/setup_app_%d_%m_%Y.log')
logging.basicConfig(filename=LOG_FILENAME, filemode='a', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)

python_major_version = sys.version_info.major

if python_major_version <3:
    logger.critical("Version Issue : Please install Python Version 3 or greater to execute this script")
else:
    logger.debug("Correct Python Version Found")
    logger.debug("Preparing Script Environment")
    setupEnvironment = SetupEnvironment(logger, os)
    setupEnvironment.installAndUnpgradeLibraries()
    logger.debug("Environment Setup Completed")
    
    
    