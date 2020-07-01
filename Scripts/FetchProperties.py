from jproperties import Properties
from configobj import ConfigObj

class FetchProperties :

    def main(self) :
        configuration = Properties()
        with open('../Config/Scraping.properties', 'rb') as config_file:
            configuration.load(config_file)
        return configuration

    def write_properties(self, updatedDate) :
        config = ConfigObj("../Config/Scraping.properties")
        config['searchDate'] = str(updatedDate)
        config.write()