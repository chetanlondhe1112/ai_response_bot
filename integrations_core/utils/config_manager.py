import toml

class ConfigLoader:
    def __init__(self):
        pass
    
    def get_config(self,config_path):
        with open(config_path, 'r') as file:
            self.__config = toml.load(file)
        return self.__config