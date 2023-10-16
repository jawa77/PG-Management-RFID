import json
import os

def get_config(key):
    # Using os.path to build an absolute path to the config.json file
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
    with open(config_file, "r") as file:
        config = json.load(file)

    file.close()
    
    if key in config:
        return config[key]
    else:
        raise Exception("Key {} is not found in config.json".format(key))
    