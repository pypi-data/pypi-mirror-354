import os
from akamai.edgegrid import EdgeGridAuth
import requests
from configparser import ConfigParser

def load_edgerc(edgerc_path="~/.edgerc", section="default"):
    path = os.path.expanduser(edgerc_path)
    config = ConfigParser()
    config.read(path)
    if section not in config:
        raise ValueError(f"Section [{section}] not found in {path}")
    return {
        "client_token": config[section]["client_token"],
        "client_secret": config[section]["client_secret"],
        "access_token": config[section]["access_token"],
        "host": config[section]["host"]
    }
