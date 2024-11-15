import os
from github import Github
import requests
import subprocess


def execute_install():
    command = [installer_path] + install_arguments
    try:
        subprocess.run(command, check=True)
        print("Installation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")


# Replace 'your_token_here' with your actual PAT
token = ""
repoName = "taskscape/Timesheets"
installer_path = r""
website_name = "MyWebsite"
configure_iis = True
install_dir = r"C:\TimeSheetsApp"

# Command-line arguments for the installer
install_arguments = [
    "/VERYSILENT",
    "/NORESTART",
    f"/WEBSITENAME={website_name}",
    f"/CONFIGUREIIS={'yes' if configure_iis else 'no'}",
    f'/DIR={install_dir}'
]

g = Github(token)

# Replace 'owner' and 'repo_name' with the repository's owner and name
repo = g.get_repo(repoName)

# Get the latest release
latest_release = repo.get_latest_release()

# Download each asset in the release using the GitHub API endpoint
for asset in latest_release.get_assets():
    asset_name = asset.name
    if os.path.exists(asset_name):
        print(f"{asset_name} already exists in the current folder. Skipping download and installation.")
        continue
    asset_id = asset.id

    download_url = f"https://api.github.com/repos/{repoName}/releases/assets/{asset_id}"

    # Send a GET request to the GitHub API with the correct headers for asset download
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/octet-stream'  # Required for the GitHub API to return binary data
    }
    response = requests.get(download_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content to a file
        with open(asset_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {asset_name}")
        if asset_name.startswith("TimeSheets") and asset_name.endswith(".exe"):
            installer_path = asset_name
            execute_install()
            break
    else:
        print(f"Failed to download {asset_name}: {response.status_code} {response.text}")



