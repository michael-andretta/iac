### Import Libraries ###
import datetime
import ipaddress
import json
import os
import re
import requests
import yaml

### Global Variables ###
# Unicode Characters & Formatting
red_x = "&#10060;"
green_check = "&#9989;"
warning = ":warning:"
html_bold_start = "<b>"
html_bold_end = "</b>"
github_underline_start = "<ins>"
github_underline_end = "</ins>"

# Global List/Dict Variables
all_pr_data = {}
pr_comment_list = []
files_changed_in_pr = []
files_with_issues = {}
ip_variables_global = {}
all_vars = {}

### GitHub Environment ###
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
if GITHUB_WORKSPACE is not None:
    print("### Running in GitHub Mode ###")
    ### Debug Mode
    _DEBUG = False
    ### GitHub Variables
    GHPATH = GITHUB_WORKSPACE + "/"
    GH_ROOT_DIR = "/"
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    PULL_NUMBER = os.getenv("PULL_NUMBER")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GH_HTTP_HEADERS = {"Authorization": "token " + GITHUB_TOKEN}
    GITHUB_BRANCH = os.getenv("GITHUB_HEAD_REF")
    GH_AUTOMATION_USERNAME = "github-actions[bot]"
    GH_MAIN_BRANCH = "/main/"
    GH_CURRENT_BRANCH = "/"
    ### Microsegmentation Variables
    MICROSEG_REPO = GHPATH + "/microsegmentation_guidelines"
    MICROSEG_YAML = "/msg_rules/rules_for_msg.yml"
    SAE_COMMENTS = "/msg_rules/sae_comments.yml"
    ### Azure Service Tag Variables
    SERVICETAG_REPO = GHPATH + "/network-actions/azure_servicetag_generator"
    SERVICETAG_JSON = "/azure_service_tags.json"
    ### Network Schema Variables
    NETWORK_SCHEMA_REPO = GHPATH + "/network-actions/nsg_checker_v2/schemas"
    NETWORK_SCHEMA_YAML = "/network_schema.yml"
    ### ODP Global NSG Variables
    GLOBAL_DEFINITIONS = "global_vars/global_definitions.yml"
    GLOBAL_DED_DESKTOPS = "global_vars/dedicated_desktops.yml"

else:
    print("### Running in Local Mode ###")
    # from env_vars.secrets import local_gh_token
    ### Debug Mode
    _DEBUG = False
    ### GitHub Variables
    GHPATH = os.path.dirname(os.path.realpath(__file__)) + "/"
    GH_ROOT_DIR = GHPATH
    # GITHUB_TOKEN = local_gh_token
    PULL_NUMBER = "109"
    GITHUB_REPOSITORY = "officedepot/network-actions" # "officedepot/network_scripts"
    # GH_HTTP_HEADERS = {"Authorization": "token " + GITHUB_TOKEN}
    GITHUB_BRANCH = "local_branch"
    GH_AUTOMATION_USERNAME = "svc-od-git-network"
    GH_MAIN_BRANCH = "/main/"
    GH_CURRENT_BRANCH = "/test_files/"
    ### Microsegmentation Variables
    MICROSEG_REPO = GHPATH
    MICROSEG_YAML = "/test_files/rules_for_msg.yml"
    SAE_COMMENTS = "/test_files/sae_comments.yml"
    ### Azure Service Tag Variables
    SERVICETAG_REPO =  GHPATH + "../azure_servicetag_generator"
    SERVICETAG_JSON = "/azure_service_tags.json"
    ### Network Schema Variables
    NETWORK_SCHEMA_REPO = GHPATH
    NETWORK_SCHEMA_YAML = "/schema.yml"
    ### ODP Global NSG Variables
    GLOBAL_DEFINITIONS = "global_vars/global_definitions.yml"
    GLOBAL_DED_DESKTOPS = "global_vars/dedicated_desktops.yml"

# Description: Function to standardize logging format
def logger(log_message, level="UNKNOWN"):
    if level == "GH_ACTION":
        print('##########################')
        print(f'# {log_message} ')
        print('##########################')
    elif level == "OK":
        print(f'OK -- {log_message}')
    elif level == "INFO":
        print(f'INFO -- {log_message}')
    elif level == "WARNING":
        print(f'WARNING -- {log_message}')
    elif level == "ERROR":
        print(f'ERROR -- {log_message}')
    elif level == "CRITICAL":
        print(f'CRITICAL -- {log_message}')
    elif level == "DEBUG" and _DEBUG == True:
        print(f'DEBUG -- {log_message}')
    elif level == "NONE":
        print(f'{log_message}')
    elif level == "EXCEPTION":
        print(f'EXCEPTION -- {log_message}')
    elif level == "UNKNOWN":
        print(f'UNKNOWN -- {log_message}')

# Description: Function to load YAML file types
def load_yaml_file(file, path=GHPATH, failed_pr=False, silent=False):
    global failed_pr_linting

    try:
        with open(path + file, 'r') as stream:
            if silent:
                return yaml.safe_load(stream)
            else:
                logger(f"Successfully loaded YAML file {path + file}", "OK")
                return yaml.safe_load(stream)
    except Exception as e:
        logger(f"Unable to load YAML file {path + file} -- {e}", "EXCEPTION")
        logger(f"Unable to load YAML file {path + file} -- {e}", "DEBUG")
        if failed_pr == True:
            failed_pr_linting = True
            pr_comment_list.append(f" {red_x} Error: Unable to parse NSG file " + path + file + " - " + str(e))
        return {}

# Description: Function to Ignore Files
# def ignore_file(file):
#     # print(f"file: {file}")
#     match = ""
#     if file.split("\\")[-1] in jpcconf['ignore']:
#         match = file.split("\\")[-1]
#     elif file.split("/")[-1] in jpcconf['ignore']:
#         match = file.split("/")[-1]
#     for ignore in jpcconf['ignore']:
#         # print(f"file: {file} - ignore: {ignore}")
#         if ignore in file:
#             match = ignore
#             break
#     if match != "":
#         print(f"Ignoring file: {file} - matched: {match}")
        return True

def load_files_changed_in_pr():
    # Load Network Schema
    network_schema = load_yaml_file(NETWORK_SCHEMA_YAML, NETWORK_SCHEMA_REPO)

    files = [
        'global_vars/global_definitions.yml',
        'od-networktools/vars/subscription_rules.yml',
        'od-networktools/roles/storage/vars/main.yml',
        '.github/workflows/azure_service_tag_generator.yml'
        ]

    try:
        for file in files:
            for ignored in network_schema['ignore']:
                if ignored in file:
                    logger(f"Ignoring file: {file} - matched: {ignore}", "INFO")
                    break
            else:
                logger(f"Adding file: {file} to 'files_changed_in_pr' list", "INFO")
                files_changed_in_pr.append(file)

    except Exception as e:
        logger(f"Failed to get changed files in PR -- {e}", "EXCEPTION")
        logger(f"Failed to get changed files in PR -- {e}", "DEBUG")

if __name__ == "__main__":
    # Load Files Changed in PR
    load_files_changed_in_pr()

