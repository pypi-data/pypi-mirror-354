from Config_parser.configService import ConfigLoader
from Config_parser.dictHelper import get_nested


class Nestedservice:
    def __init__(self):
        self.config = ConfigLoader().get_config()

    def getNestedKey(self,path):
        #db_host = self.config.get("data_source", {}).get("connection", {}).get("host")
        host = get_nested(self.config, path)
        return host

