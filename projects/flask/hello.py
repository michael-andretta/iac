### Import Libraries ###
from flask import Flask
import os

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

### Logger Configuration ###
def logger(message, level="UNKNOWN"):
    if level == "HEADER":
        print('##########################')
        print(f'# {message} ')
        print('##########################')
    elif level == "OK":
        print(f'OK - {message}')
    elif level == "INFO":
        print(f'INFO - {message}')
    elif level == "WARNING":
        print(f'WARNING - {message}')
    elif level == "EXCEPTION":
        print(f'EXCEPTION - {message}')
    elif level == "ERROR":
        print(f'ERROR - {message}')
    elif level == "DEBUG" and _DEBUG == True:
        print(f'DEBUG - {message}')
    elif level == "UNKNOWN":
        print(f'UNKNOWN LOGGING LEVEL - {message}')
    elif level == "NONE":
        print(f'{message}')

### Create Flask Site ###
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"
