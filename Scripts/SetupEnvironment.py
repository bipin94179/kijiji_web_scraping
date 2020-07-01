import sys
import platform

class SetupEnvironment:

    def __init__(self, logger, os) :
        self.logger = logger
        self.os = os

    def installAndUnpgradeLibraries(self) :
        try :
            self.logger.debug("Updating pip version to support the Script functionality")
            pip_install_stream = self.os.popen('python -m pip install --upgrade pip')
            self.logger.debug(pip_install_stream.read())
            self.logger.debug("Preparing for Selenium Installation")
            selenium_install_stream = self.os.popen('pip install selenium')
            self.logger.debug(selenium_install_stream.read())
            self.logger.debug("Preparing for Requests Installation")
            requests_install_stream = self.os.popen('pip install requests')
            self.logger.debug(requests_install_stream.read())
            self.logger.debug("Preparing for BeautifulSoup Installation")
            beautifulSoap_install_stream = self.os.popen('pip install bs4')
            self.logger.debug(beautifulSoap_install_stream.read())
            self.logger.debug("Preparing for JProperties Installation")
            jproperties_install_stream = self.os.popen('pip install jproperties')
            self.logger.debug(jproperties_install_stream.read())
            self.logger.debug("Preparing for ConfigObj Installation")
            configobj_install_stream = self.os.popen('pip install configobj')
            self.logger.debug(configobj_install_stream.read())    
        except Exception :
            self.logger.error("Environment could not be setup due to System Error. Please provide required privileges to run the Script")
            sys.exit()
