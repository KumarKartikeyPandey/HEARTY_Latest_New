from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

SESSION_TIMEOUT = timedelta(minutes=30)  # Session timeout set to 30 minutes

# Hardcoded credentials
VALID_EMAIL = "pawan@gmail.com"
VALID_PASSWORD_HASH = bcrypt.generate_password_hash("Pawan@123").decode('utf-8')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check hardcoded credentials
        if email == VALID_EMAIL and bcrypt.check_password_hash(VALID_PASSWORD_HASH, password):
            session.clear()  # Reset session on login
            session['user_id'] = 1  # Dummy user ID
            session['username'] = 'Pawan'
            session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            next_page = session.pop('next', url_for('index'))  # Redirect to stored next page or index
            return redirect(next_page)
        else:
            flash("Invalid email or password!", "danger")

    return render_template('login.html')

@auth.route('/logout')
def logout():
    """Logout and destroy session"""
    session.clear()
    return redirect(url_for('index'))

def is_session_expired():
    """Check if session is expired or should be invalidated"""
    if 'last_activity' in session:
        last_activity = datetime.strptime(session['last_activity'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() - last_activity > SESSION_TIMEOUT:
            session.clear()  # Invalidate session on timeout
            return True
    session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Update session activity
    return False
