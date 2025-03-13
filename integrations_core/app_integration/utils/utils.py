# Utils module to manage 
# 1.File loading

import toml
from toml import TomlDecodeError

def load_config(filepath=str):
    """load_config method loads the configuration file

    Args:
        filepath (str): configuration toml file path. Defaults to str.
    """
    try:
        if filepath != None:
            return True,toml.load(filepath)
        else:
            return False,None
    except TomlDecodeError as e:
        print(f"Failed to Load config file : {e}")
        return False,e
