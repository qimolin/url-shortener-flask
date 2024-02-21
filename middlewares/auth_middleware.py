from functools import wraps
from flask import request
from modules.url import URL
from utils.auth_utils import verify_auth

def auth_required(return_user_id=False, check_ownership=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract JWT token from request headers
            token = request.headers.get('Authorization')
            if not token:
                return {'message': 'Token is missing'}, 401

            # Extract the JWT token from the Authorization header
            token = token.split(' ')[1] if token.startswith('Bearer ') else token
            
            # Verify authentication
            result = verify_auth(token)
            valid = result.get('valid')
            
            if not valid:
                return {'error': 'Invalid JWT token'}, 403

            # Extract user ID from the decoded token
            user_id = result.get('user_id')

            if check_ownership:
                url_service = URL()
                shortened_url_id = kwargs.get('id')
                if not url_service.url_exists(shortened_url_id):
                    return {'error': 'URL does not exist'}, 404
                if not url_service.is_owner(user_id, shortened_url_id):
                    return {'error': 'User is not the owner of the URL'}, 403

            if return_user_id:
                return func(user_id, *args, **kwargs)  # Pass user_id to the wrapped function
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
