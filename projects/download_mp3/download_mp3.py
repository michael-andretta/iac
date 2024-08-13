### Import Libraries ###
import requests
import os
from pytube import YouTube
from env_vars.secrets import gh_token

### Define Gobal Variables ###
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
    elif level == "ERROR":
        print(f'ERROR - {log_message}')
    elif level == "DEBUG" and _DEBUG == True:
        print(f'DEBUG - {log_message}')
    elif level == "UNKNOWN":
        print(f'UNKNOWN LOGGING LEVEL - {log_message}')
    elif level == "NONE":
        print(f'{log_message}')

### Load in List of Download URL's ###
def load_music_list(file, path=GHPATH):
    try:
        with open(path + file, 'r') as stream:
            music_list = stream.readlines()
            return music_list
    except Exception as e:
        logger(f"Error loading {file}", "ERROR")
        logger(f"Message: {e}", "DEBUG")
        return None

if __name__ == "__main__":
    music = load_music_list("urls.txt")
    ### Read in List of URL's ###
    for url in music:
        try:
            yt = YouTube(url)
            print(f"Downloading: {yt.title}")
            ### Exrtact Audio Only ###
            audio = yt.streams.filter(only_audio=True).first()
            ### Download Audio ###
            out_file = audio.download(output_path=local_directory)
            ### Save File ###
            base, ext = os.path.splitext(out_file)
            new_file = base + ".mp3"
            os.rename(out_file, new_file)
            ### Print Results ###
            logger(f"Downloaded {yt.title} to {new_file}", "OK")

        except Exception as e:
            logger(f"Message: {e}", "DEBUG")
            continue
