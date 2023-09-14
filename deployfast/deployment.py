import os
import requests
import subprocess
import shutil

# Replace with your GitHub username, repository name, and token
username = ""
repository_name = ""
token = ""

def create_github_repo(username, repository_name, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "name": repository_name,
        "auto_init": True
    }

    response = requests.post(f"https://api.github.com/user/repos", headers=headers, json=data)

    if response.status_code == 201:
        print(f"Repository '{repository_name}' created successfully.")
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(response.text)

def clone_github_repo(username, repository_name):
    repo_url = f"https://github.com/{username}/{repository_name}.git"
    local_directory = f"./{repository_name}"

    subprocess.run(["git", "clone", repo_url, local_directory])
    print(f"Repository '{repository_name}' cloned locally.")

if __name__ == "__main__":
    create_github_repo(username, repository_name, token)
    clone_github_repo(username, repository_name)

    
    project_directory = ""  # Replace with your project directory name
    local_repo_directory = f"./{repository_name}/{project_directory}"

    if not os.path.exists(local_repo_directory):
        os.makedirs(local_repo_directory)

    for item in os.listdir(project_directory):
        source = os.path.join(project_directory, item)
        destination = os.path.join(local_repo_directory, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    os.chdir(f"./{repository_name}")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Initial commit"])
    subprocess.run(["git", "push"])

    print("Project files pushed to GitHub.")