# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, make_response, redirect
import requests
import json

# locals
from .routes import routes
from app import db
from database import User, Harvest, authorize_required, login_required, admin_required, Events

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
admin_bp = Blueprint("admin", __name__)

# ------------------------ VIEWS ----------------------------- #
# Users
@admin_bp.route(routes["admin"]["users"], methods=['GET', 'POST'])
@login_required
@admin_required
def users(current_user = None):
  # Variables that the template will use to render
  error = None

  # We obtain all available users to render them in the list
  all_users = User.query.all()
  all_harvests = Harvest.query.all()

  # Search bar options
  search_bar = {
    "enabled": True,
    "options": ["Usuario", "Rol"],
    "selected": "Usuario",
    "value": ""
  }

  if request.method == 'POST':
    # See what action we want to achieve
    if 'action-type' in request.form and request.form['action-type'] == 'create':
      form = request.form

      # We validate if empty fields
      if not (form['username'] and form['password']):
        error = 'No hay nombre de usuario o contraseña al enviar la solicitud.'
      else:
        # We confirm the username isn't already taken
        user = User.query.filter_by(username=form['username']).first() 

        if user is None:
          default_user = User(
            username=form['username'],
            password=form['password'],
            name=form['name'],
            last_name=form['last_name'],
            role=form['role']
          )
          db.session.add(default_user)
          db.session.commit()

          return redirect('/admin' + routes["admin"]["users"])
        else:
          error = 'ERROR: nombre de usuario no dispobible.'

    # We see the case for the search bar functionality
    elif 'action-type' in request.form and request.form['action-type'] == 'search':
      # Search values
      search_bar['value'] = request.form['search_value']

      # Search bar for possible cases
      if request.form['search_option'] == 'Usuario':
        search_bar['selected'] = 'Usuario'
        all_users = User.query.filter(User.username.like('%' + request.form['search_value'] + '%')).all()
      elif request.form['search_option'] == 'Rol':
        search_bar['selected'] = 'Rol'
        all_users = User.query.filter(User.role.like('%' + request.form['search_value'] + '%')).all()

    # We edit the user
    elif 'user-id' in request.form:
      # default case is editing a user
      # TODO:See what guards can i create with this
      response = requests.put(
        'http://localhost:5000/admin/users/' + request.form['user-id'],
        json={
          'username': request.form['username'],
          'name': request.form['name'],
          'last_name': request.form['last_name'],
          'role': request.form['role']
        },
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )
      return redirect('/admin' + routes["admin"]["users"])

  return render_template('users.html', all_users=all_users, all_harvests=all_harvests, error=error, search_bar=search_bar)

# logger
@admin_bp.route(routes["admin"]["logger"], methods=['GET', 'POST'])
@login_required
@admin_required
def logger(current_user = None):
  # Variables that the template will use to render
  error = None

  # We obtain all available users to render them in the list
  all_events = Events.query.all()

  return render_template('logger.html', events=all_events, error=error)


# ------------------------ CONTROLLERS ----------------------------- #
# Edit Users
@admin_bp.route('/users/<int:idx>', endpoint="edit", methods=['PUT'])
@authorize_required
def users(idx):
  # We get the user we want to update
  user = User.query.filter_by(id=idx).first()

  # Parse the answeer from the request
  data = json.loads(request.data)

  # We check if the user exists
  if user is None:
    return make_response('User not found.', 404)
  else: 
    # Update the user according
    if data['username']:
      user.username = data['username']
    if data['name']:
      user.name = data['name']
    if data['last_name']:
      user.last_name= data['last_name']
    if (data['role']):
      user.role = data['role']
    
    # We commit the changes to the database
    db.session.commit()

    return make_response('User updated.', 200)