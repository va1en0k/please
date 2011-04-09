import os
import ConfigParser

def get_config():    
    config = ConfigParser.ConfigParser()
    config.read(['/etc/pyplease.conf',
                 os.path.expanduser('~/.pyplease'),
                 os.path.join(os.path.abspath(__file__),
                              '.pyplease')])

    return config

CONFIG = get_config()
