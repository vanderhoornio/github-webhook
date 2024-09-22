import hmac
import hashlib
from functools import wraps

from flask import request, abort

from poller.api.utilities.config import Config

config = Config()

def verify_github_signature(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        # Get the signature from the headers
        signature = request.headers.get('X-Hub-Signature-256')
        if signature is None:
            abort(400, 'Missing signature')
        
        # The body of the request that needs to be signed
        data = request.get_data()
        
        # Compute the HMAC hex digest using the GitHub secret and SHA-256
        computed_signature = 'sha256=' + hmac.new(
            config.github_webhook_secret.encode(),
            data,
            hashlib.sha256
        ).hexdigest()
        
        # Compare the signatures (using hmac.compare_digest for security)
        if not hmac.compare_digest(computed_signature, signature):
            abort(400, 'Invalid signature')
        
        # If signatures match, proceed to the original function
        return f(*args, **kwargs)
    return decorated


def validate_watchlist(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        
        # If signatures match, proceed to the original function
        return f(*args, **kwargs)
    return decorated