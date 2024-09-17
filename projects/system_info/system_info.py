### Import Libraries ###
import requests
import os
import yaml
import json
import platform
### Import Secrets from env_vars dir secrets.py file ###
from env_vars.secrets import gh_token, password

### Define Variables ###
os_version = platform.system()
if os_version == "Windows":
    local_directory = os.path.dirname(os.path.realpath(__file__)) + "\\"
elif os_version in ["Linux", "Darwin"]:
    local_directory = os.path.dirname(os.path.realpath(__file__)) + "/"
else:
    local_directory = os.path.dirname(os.path.realpath(__file__)) + "/"

### Define GitHub Environment ###
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
if GITHUB_WORKSPACE is not None:
    print("### Running in GitHub Mode ###")
    _DEBUG = False
    GHPATH = GITHUB_WORKSPACE + "/"
    GH_ROOT_DIR = "/"
    GITHUB_TOKEN = os.getenv("GITSECRET")
    PULLNUMBER = os.getenv("PULLNUMBER")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

else:
    print("### Running in Local Mode ###")
    _DEBUG = True
    GHPATH = os.path.dirname(os.path.realpath(__file__)) + "/"
    GH_ROOT_DIR = GHPATH
    GITHUB_TOKEN = None # "" ###
    PULLNUMBER = None # "22"
    GITHUB_REPOSITORY = None # "officedepot/network_scripts"

### Define Logging Function ###
def logger(log_message, level="UNKNOWN"):
    if level == "GH_ACTION":
        print('##########################')
        print(f'# {log_message} ')
        print('##########################')
    elif level == "OK":
        print(f'OK - {log_message}')
    elif level == "INFO":
        print(f'INFO - {log_message}')
    elif level == "WARNING":
        print(f'WARNING - {log_message}')
    elif level == "EXCEPTION":
        print(f'EXCEPTION - {log_message}')
    elif level == "ERROR":
        print(f'ERROR - {log_message}')
    elif level == "DEBUG" and _DEBUG == True:
        print(f'DEBUG - {log_message}')
    elif level == "UNKNOWN":
        print(f'UNKNOWN LOGGING LEVEL - {log_message}')
    elif level == "NONE":
        print(f'{log_message}')

### Load in List of Download URL's ###
def load_yaml_file(file, path=GHPATH):
    try:
        with open(path + file, 'r') as stream:
            yaml_data = yaml.safe_load(stream)
            return yaml_data
    except Exception as e:
        logger(f"Error loading {file}", "EXCEPTION")
        logger(f"Error loading {file}: {e}", "DEBUG")
        return None

def load_json_file(file, path=GHPATH):
    try:
        with open(path + file, 'r') as stream:
            json_data = json.load(stream)
            return json_data
    except Exception as e:
        logger(f"Error loading {file}", "EXCEPTION")
        logger(f"Error loading {file}: {e}", "DEBUG")
        return None

if __name__ == "__main__":
    ### Sample Code ###
    logger(f"Starting Script Execution", "GH_ACTION")

    logger(f"Local Directory: {local_directory}", "INFO")

    ### Print out System Information ###
    logger(f"Platform: {platform.platform()}", "INFO")
    logger(f"System: {platform.system()}", "INFO")
    logger(f"Architecture: {platform.architecture()}", "INFO")
    logger(f"Node: {platform.node()}", "INFO")
    logger(f"Machine: {platform.machine()}", "INFO")
    logger(f"Release: {platform.release()}", "INFO")
    logger(f"Version: {platform.version()}", "INFO")
    logger(f"Processor: {platform.processor()}", "INFO")
    logger(f"Mac Version: {platform.mac_ver()}", "INFO")
    logger(f"Python Version: {platform.python_version()}", "INFO")
    logger(f"Python Compiler: {platform.python_compiler()}", "INFO")
    logger(f"Python Build: {platform.python_build()}", "INFO")
    logger(f"Python Implementation: {platform.python_implementation()}", "INFO")
