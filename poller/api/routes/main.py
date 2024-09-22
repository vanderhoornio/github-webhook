from flask import Blueprint, request, jsonify

from poller.api.utilities.decorators import verify_github_signature
from poller.api.events.releases import handle_release_event
from poller.api.utilities.config import Config

config = Config()

main = Blueprint('main', __name__)


@main.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello world'})


@main.route('/github/webhook', methods=['POST'])
@verify_github_signature
def github_webhook():
    
    payload = request.json
    
    # Perform check
    repository_info = payload.get('repository')
    repository_name = repository_info.get('full_name')
    
    if repository_name not in config.watchlist:
        return jsonify({'status': 'ignored', 'message': 'Repository is not in watchlist'}), 200
    
    # Handle release events
    event = request.headers.get('X-GitHub-Event')
    if event == 'release':
        status, message = handle_release_event(payload, repository_name)
        if status == 'success':
            return jsonify({'status': status, 'message': message}), 200
        else:
            return jsonify({'status': status, 'message': message}), 400
    
    # If it's not a release event, only acknowledge the webhook
    return jsonify({'status': 'ignored', 'message': 'Event not handled'}), 200
    
    


def register(app):
    """
    Register the MAIN Blueprint with the Flask application.
    
    Args:
        app (Flask): The Flask application instance to which the MAIN Blueprint will be registered.
    """
    app.register_blueprint(main)