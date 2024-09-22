import time
import json
import requests


from poller.api.utilities.config import Config

config = Config()

    
def handle_release_event(payload, repository_name):
    """Handles the payload when an event matches 'release' and then calls post_release_notification"""
    action = payload.get('action')
    release_info = payload.get('release')
    
    
    if action == 'published' and release_info:
        tag_name = release_info.get('tag_name')
        release_url = release_info.get('html_url')
        published_at = release_info.get('published_at')
        
        print(f"New release detected: {tag_name} at {release_url}")
        print(repository_name)
        
        # Save release to config.json
        config.latest_releases[repository_name] = {
            'tag_name': tag_name,
            'published_at': published_at,
            'release_url': release_url
            }
        config.save_latest_release()
        
        # Create the workflow engine
        
        success, message = post_release_notification(tag_name, release_url)
        
        if success:
            return 'success', message
        else:
            return 'failed', message
    else:
        return 'ignored', 'No action taken for this release event'
    
    
def post_release_notification(tag_name, release_url):
    """Sends a POST request with the release information"""
    url = "https://webhook.site/da0642cc-9f02-4089-b85e-c3d6b5f838a2"
    headers = {'Content-Type': 'application/json'}
    
    data = {
        'release_tag': tag_name,
        'release_url': release_url
    }
    
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        # Return a tuple with success status and message
        if response.status_code == 200:
            print(f"Successfully notified external service about release {tag_name}")
            return True, f"Successfully notified external service about release {tag_name}"
        else:
            print(f"Failed to notify external service: {response.status_code}")
            return False, f"Failed to notify external service: {response.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle network/connection errors
        print(f"Error sending POST request: {str(e)}")
        return False, f"Error sending POST request: {str(e)}"
    