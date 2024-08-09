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
    "Authorization": "Bearer " + gh_token
}

### Define GitHub Environment ###
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
if GITHUB_WORKSPACE is not None:
    print("### Running in GitHub Mode ###")
    GHPATH = GITHUB_WORKSPACE + "/"
    GH_ROOT_DIR = "/"
    GITHUB_TOKEN = os.getenv("GITSECRET")
    PULLNUMBER = os.getenv("PULLNUMBER")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

else:
    print("### Running in Local Mode ###")
    GHPATH = os.path.dirname(os.path.realpath(__file__)) + "/"
    GH_ROOT_DIR = GHPATH
    GITHUB_TOKEN = None # "" ###
    PULLNUMBER = None # "22"
    GITHUB_REPOSITORY = None # "officedepot/network_scripts"

### Define Logging Function ###
def logger(log_message, level="WARNING"):
    if level == "GH_ACTION":
        print('##########################')
        print(f'# {log_message} ')
        print('##########################')
    elif level == "INFO":
        print(f'INFO - {log_message}')
    elif level == "ERROR":
        print(f'ERROR - {log_message}')
    elif level == "WARNING":
        print(f'WARNING - {log_message}')
    elif level == "DEBUG":
        print(f'DEBUG - {log_message}')
    elif level == "POUNDSIGN":
        print('##########################')
    elif level == "NONE":
        print(f'{log_message}')
    else:
        print(f'##### {log_message} #####')

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

### Main ###
if __name__ == "__main__":
    repo = "michael-andretta/iac"
    current_labels = get_gh_labels(repo)

    ### Print Current Labels ###
    logger(f"Current Labels for {repo}:", "GH_ACTION")
    # logger(f"Current Label List: {current_labels}", "NONE")
    for label in current_labels:
        logger(f"Current Label: {label['name']} | HEX code: #{label['color']} | Description: {label['description']}", "INFO")

    ### Load Labels from YAML ###
    logger("Proposed Labels from YAML", "GH_ACTION")
    proposed_labels_yml = load_yaml_file("labels.yml")
    # logger(f"YAML: {proposed_labels_yml}", "INFO")
    ### Show Proposed Labels Data Types ###
    for label in proposed_labels_yml if proposed_labels_yml is not None else []:
        logger(f"Proposed Label: Name: {label['name']} | HEX code: {label['color']} | Description: {label['description']}", "INFO")

    ### Creare New Labels If they are not already in the repo ###
    logger("Creating/Updating Labels", "GH_ACTION")
    for label in proposed_labels_yml if proposed_labels_yml is not None else []:
        try:
            ### If Label Does Not Exist Create It ###
            if label['name'] not in [x['name'] for x in current_labels]:
                create_gh_label(repo, label['name'], label['description'], label['color'])

            ### If Label Exists Update It ###
            if label['name'] in [x['name'] for x in current_labels] and \
                (label['description'] != current_labels[[x['name'] for x in current_labels].index(label['name'])]['description'] or \
                    label['color'] != current_labels[[x['name'] for x in current_labels].index(label['name'])]['color']):
                update_gh_label(repo, label['name'], label['description'], label['color'])

            else:
                logger(f"Label: {label['name']} already exists with the same description and color", "INFO")

        except Exception as e:
            logger(f"Error creating label: {label['name']} -- {e}", "ERROR")

    ### Delete Labels That Are Not In The YAML but in Current ###
    try:
        if len(proposed_labels_yml) < len(current_labels):
            logger("Deleting Labels", "GH_ACTION")
            for label in current_labels:
                if label['name'] not in [x['name'] for x in proposed_labels_yml]:
                    delete_gh_label(repo, label['name'])
    except Exception as e:
        logger(f"No Labels to Delete | labels.yml is empty", "WARNING")

    if proposed_labels_yml is None:
        logger("Deleting All Labels", "GH_ACTION")
        for label in current_labels:
            delete_gh_label(repo, label['name'])
