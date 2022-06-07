# import the Flask instances
from flask import Blueprint, render_template, request, redirect, url_for

from .routes import routes

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
            return redirect(url_for('home'))
    return render_template('login.html', error=error)