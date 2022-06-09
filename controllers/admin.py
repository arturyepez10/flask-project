# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, make_response, redirect
import requests
import json

# locals
from .routes import routes
from app import db
from database import User, authorize_required, login_required

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
admin_bp = Blueprint("admin", __name__)

# ------------------------ VIEWS ----------------------------- #
# Users
@admin_bp.route(routes["admin"]["users"], methods=['GET', 'POST'])
@login_required
def users(current_user = None):
  # We obtain all available users to render them in the list
  all_users = User.query.all()

  if request.method == 'POST':
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

  return render_template('users.html', all_users=all_users)


# ------------------------ CONTROLLERS ----------------------------- #
# Users
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