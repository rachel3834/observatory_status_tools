import json

def read_config(path_to_config_file):

    if path.isfile(path_to_config_file) == False:
        raise IOError("No config file found at given location: "+path_to_config_file)

    config_file = open(path_to_config_file,'r')

    config_dict = json.load(config_file)

    config_file.close()

    return config_dict
