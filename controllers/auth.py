# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, redirect, url_for, make_response, session

# locals
from .routes import routes
from database import login_required

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
auth_bp = Blueprint("auth", __name__)

# ------------------------ VIEWS ----------------------------- #
# Login
@auth_bp.route(routes["auth"]["login"], methods=['GET', 'POST'])
def login():
    # Variables that the template will use to render
    error = None

    # Handled of the post request done to this endpoint
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = { 'login': 'Invalid Credentials. Please try again.'}
        else:
            session['current_user'] = { 'username': request.form['username'], 'password': request.form['password'] }
            return redirect('/admin' + routes["admin"]["users"])

    # We check if the user already has a session token
    if 'current_user' in session:
        return redirect('/admin' + routes["admin"]["users"])
    return render_template('login.html', error=error)

# ------------------------ CONTROLLERS ----------------------------- #
# Logout
@auth_bp.route(routes["auth"]["logout"], methods=['GET'])
def logout():
    # remove the username from the session
    session.pop('current_user')
    return redirect('/')