# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, Response, render_template, request, redirect, session, Response

# locals
from .routes import routes
from database import User

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
auth_bp = Blueprint("auth", __name__)

# ------------------------ VIEWS ----------------------------- #
# Login
@auth_bp.route(routes["auth"]["login"], methods=['GET', 'POST'])
def login():
    # Variables that the template will use to render
    error = None
    code = 200

    # Handled of the post request done to this endpoint
    if request.method == 'POST':
        if not (request.form['username'] and request.form['password']):
            error = { 'login': 'Campo(s) vacio(s). Por favor, llena la información.' }
            code = 400
        else:
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None:
                if user.password == request.form['password']:
                    session['current_user'] = { 'username': request.form['username'], 'password': request.form['password'] }
                    return redirect('/admin' + routes["admin"]["users"])
                else:
                    error = { 'login': 'Contraseña incorrecta.' }
                    code = 400
            else:
                error = { 'login': 'Usuario no encontrado.' }
                code = 404

    # We check if the user already has a session token
    if 'current_user' in session:
        return redirect('/admin' + routes["admin"]["users"])
    return render_template('login.html', error=error), code

# ------------------------ CONTROLLERS ----------------------------- #
# Logout
@auth_bp.route(routes["auth"]["logout"], methods=['GET'])
def logout():
    # remove the username from the session
    session.pop('current_user')
    return redirect('/')