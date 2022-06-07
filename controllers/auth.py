# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, redirect, url_for, make_response, session

# locals
from .routes import routes
from database import login_required

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
auth_bp = Blueprint(routes["auth"]["login"], __name__)

# ------------------------ VIEWS ----------------------------- #
# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Variables that the template will use to render
    error = None

    # Handled of the post request done to this endpoint
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = { 'login': 'Invalid Credentials. Please try again.'}
        else:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect('/auth/example')
    return render_template('login.html', error=error)

# example authed app
@auth_bp.route('/example')
@login_required
def auth_example(current_user):
    return 'Congrats you are authenticated!'