### Import Libraries ###
import requests
import json
import os
import yaml
from env_vars.secrets import gh_token

### Variables ###
gh_base_url = "https://api.github.com"
owner = "michael-andretta"

headers = {
    "Authorization": gh_token
}

### Global Lists & Dictionaries ###
files_changed_in_pr = []

### Define GitHub Environment ###
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
if GITHUB_WORKSPACE is not None:
    print("### Running in GitHub Mode ###")
    _DEBUG = False
    GHPATH = GITHUB_WORKSPACE + "/"
    GH_ROOT_DIR = "/"
    GITHUB_TOKEN = os.getenv("GITSECRET")
    PULL_NUMBER = os.getenv("PULLNUMBER")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

else:
    print("### Running in Local Mode ###")
    _DEBUG = False
    GHPATH = os.path.dirname(os.path.realpath(__file__)) + "/"
    GH_ROOT_DIR = GHPATH
    GITHUB_TOKEN = gh_token
    PULL_NUMBER = 4
    GITHUB_REPOSITORY = "michael-andretta/iac"

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

### Load Labels from YAML ###
def load_yaml_file(file, path=GHPATH):
    try:
        with open(path + file, 'r') as stream:
            return yaml.safe_load(stream)
    except Exception as e:
        logger(f"Unable to load {file} -- {e}", "ERROR")
        return {}

### Functions ###
def get_gh_labels(repo):
    url = f"{gh_base_url}/repos/{repo}/labels"
    response = requests.get(url, headers=headers)
    labels = json.loads(response.text)
    return labels

def create_gh_label(repo, name, description, color):
    try:
        url = f"{gh_base_url}/repos/{repo}/labels"
        data = {
            "name": name,
            "color": color,
            "description": description
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            logger(f"Label: {name} created successfully", "INFO")
        elif response.status_code == 422:
            logger(f"Label: {name} already exists", "INFO")
        else:
            logger(f"Error creating label: {name} -- {response.text}", "ERROR")
    except Exception as e:
        logger(f"Error creating label: {name} -- {e}", "ERROR")

    return response

def update_gh_label(repo, name, description, color):
    try:
        url = f"{gh_base_url}/repos/{repo}/labels/{name}"
        data = {
            "name": name,
            "color": color,
            "description": description
        }
        response = requests.patch(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            logger(f"Label: {name} updated successfully", "INFO")
        else:
            logger(f"Error updating label: {name} -- {response.text}", "ERROR")
    except Exception as e:
        logger(f"Error updating label: {name} -- {e}", "ERROR")

    return response

def delete_gh_label(repo, name):
    try:
        url = f"{gh_base_url}/repos/{repo}/labels/{name}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            logger(f"Label: {name} deleted successfully", "INFO")
        else:
            logger(f"Error deleting label: {name} -- {response.text}", "ERROR")
    except Exception as e:
        logger(f"Error deleting label: {name} -- {e}", "ERROR")

    return response

def load_files_changed_in_pr():
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{PULL_NUMBER}/files"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            logger(f"Successfully pulled PR #{PULL_NUMBER} Data", "OK")
            payload = json.loads(response.text)
            logger(f"{payload}", "DEBUG")
            if 'filename' in payload[0]:
                for file in payload:
                    for ignored in network_schema['ignored']:
                        if ignored in file['filename']:
                            logger(f"Skipping file: {file['filename']} - matched: {ignored}", "INFO")
                            break
                    else:
                        logger(f"Adding {file['filename']} to be checked", "INFO")
                        files_changed_in_pr.append(file['filename'])
            else:
                logger(f"'filename' not found in PR files payload", "ERROR")
        else:
            logger(f"Failed to get PR files. Status code: {response.status_code}, Message: {response.text}", "ERROR")

    except Exception as e:
        logger(f"Failed to get changed files in PR -- {e}", "EXCEPTION")
        logger(f"Failed to get changed files in PR -- {e}", "DEBUG")

def add_comment_to_pr(repo, pr_number, comment):
    url = f"{gh_base_url}/repos/{repo}/issues/{pr_number}/comments"
    data = {
        "body": comment
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        logger(f"Comment added to PR #{pr_number}", "OK")
    else:
        logger(f"Failed to add comment to PR #{pr_number} -- {response.text}", "ERROR")

    return response

### Main ###
if __name__ == "__main__":
    repo = "michael-andretta/iac"

    ### Load Network Schema ###
    logger("Loading Network Schema", "GH_ACTION")
    network_schema = load_yaml_file("network_schema.yml")

    ### Load Microsegmentation Guidelines ###
    logger("Loading Microsegmentation Guidelines", "GH_ACTION")
    try:
        microsegmentation_guidelines = load_yaml_file("microsegmentation_guidelines/rules_for_msg.yml")
        sae_comments = load_yaml_file("microsegmentation_guidelines/sae_comments.yml")
        if _DEBUG:
            logger(f"Microsegmentation Rules: {microsegmentation_guidelines}", "NONE")
            logger(f"SAE Comments: {sae_comments}", "NONE")
        logger("Microsegmentation Guidelines loaded successfully", "OK")
    except Exception as e:
        logger(f"Failed to load Microsegmentation Guidelines -- {e}", "ERROR")
    
    ### Load Files Changed in PR ###
    logger("Loading Files Changed in PR", "GH_ACTION")
    load_files_changed_in_pr()

