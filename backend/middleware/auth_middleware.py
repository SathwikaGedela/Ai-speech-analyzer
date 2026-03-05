from functools import wraps
from flask import session, redirect, url_for, request, jsonify

def login_required(f):
    """
    Decorator to require login for routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # If it's an API request, return JSON error
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            # For regular routes, redirect to landing page
            return redirect(url_for('auth.landing_page'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_id():
    """
    Get current user ID from session
    """
    return session.get('user_id')

def is_authenticated():
    """
    Check if user is authenticated
    """
    return 'user_id' in session