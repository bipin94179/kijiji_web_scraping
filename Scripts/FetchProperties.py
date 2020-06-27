from jproperties import Properties

class FetchProperties :

    def main(self) :
        configuration = Properties()
        with open('../Config/Scraping.properties', 'rb') as config_file:
            configuration.load(config_file)
        return configuration