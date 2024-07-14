### Import Libraries ###
import requests
import json
from env_vars.secrets import gh_token

### Variables ###
gh_base_url = "https://api.github.com"
owner = "michael-andretta"

headers = {
    "Authorization": gh_token
}

### Functions ###
def get_gh_labels(repo):
    url = f"{gh_base_url}/repos/{repo}/labels"
    response = requests.get(url, headers=headers)
    labels = json.loads(response.text)
    return labels

def create_gh_label(repo, name, description, color):
    url = f"{gh_base_url}/repos/{repo}/labels"
    data = {
        "name": name,
        "color": color,
        "description": description
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

### Main ###
if __name__ == "__main__":
    repo = "michael-andretta/iac"
    labels = get_gh_labels(repo)
    for label in labels:    
        print(label['name'])

    ### Need If Statement to check if label exists ###
    print(create_gh_label(repo, "test", "test label via automation", "ff0000"))
