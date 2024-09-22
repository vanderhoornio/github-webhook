import os
import json
import sys

from dotenv import load_dotenv
from github import Github
from github import Auth

# Get the directory of the script that was executed (e.g., run.py)
base_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# Load the .env file from the base directory where the app is started
load_dotenv(dotenv_path=os.path.join(base_directory, '.env'))

# Set the path for config.json from the base directory
config_path = os.path.join(base_directory, 'config.json')


class Config:
    def __init__(self):
        self.path = config_path
        self.watchlist = None
        self.latest_releases = None
        self.load_config()
        
    def load_config(self):
        if not os.path.exists(self.path):
            print("Configuration file not found. Please ensure it is present in the main directory")
            exit(1)
            
        with open(self.path, 'r') as file:
            try:
                config_data = json.load(file)
                self.watchlist = config_data['watchlist']
                self.latest_releases = config_data.get('latest_releases', {})
            except json.JSONDecodeError as e:
                print(f"Encountered error parsing JSON: {e}")
                exit(1)
            except KeyError as e:
                print(f"Missing configuration key: {e}")
                exit(1)
    
    # Tokens and secrets
    @property
    def github_access_token(self) -> load_dotenv:
        """Returns the Github Access Token"""
        return os.getenv('GITHUB_ACCESS_TOKEN')
    
    @property
    def github_webhook_secret(self) -> load_dotenv:
        """Returns the Github webhook secret"""
        return os.getenv('GITHUB_WEBHOOK_SECRET')
    
    @property
    def ngrok_auth_token(self) -> load_dotenv:
        """Returns the NGROK AUTH token"""
        return os.getenv('NGROK_AUTH_TOKEN')
    
    # Github client
    @property
    def github_client(self) -> Github:
        """Retrieves the Github client"""
        auth = Auth.Token(self.github_access_token)
        return Github(auth=auth)
    
    @property
    def github_user(self) -> Github:
        """Retrieves the user for the Github client"""
        return self.github_client.get_user()
    
    # Config.json
    def save_latest_release(self):
        """Saves the latest release to config.json"""
        with open(self.path, 'r+') as file:
            config_data = json.load(file)
            config_data['latest_releases'] = self.latest_releases
            file.seek(0)
            json.dump(config_data, file, indent=4)
            file.truncate()