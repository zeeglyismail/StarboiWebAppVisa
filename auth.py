from flask import session, redirect, url_for, flash, request
from functools import wraps

# Demo login credentials - change these as needed
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin123"

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access this feature.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def is_logged_in():
    """Check if user is logged in"""
    return session.get('logged_in', False)

def login_user():
    """Log in the user"""
    session['logged_in'] = True
    session.permanent = True

def logout_user():
    """Log out the user"""
    session.pop('logged_in', None)

def check_credentials(username, password):
    """Check if provided credentials are correct"""
    return username == DEMO_USERNAME and password == DEMO_PASSWORD