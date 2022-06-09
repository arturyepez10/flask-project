# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, redirect, url_for, make_response, session

# locals
from .routes import routes
from app import db
from database import User, login_required

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
admin_bp = Blueprint("admin", __name__)

# ------------------------ VIEWS ----------------------------- #
# Users
@admin_bp.route(routes["admin"]["users"], methods=['GET', 'POST'])
@login_required
def users(current_user):
  all_users = User.query.all()
  print(request.form)

  return render_template('users.html', all_users=all_users)
