# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, redirect, url_for, make_response, session

# locals
from .routes import routes
from database import login_required

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
admin_bp = Blueprint("admin", __name__)

# ------------------------ VIEWS ----------------------------- #
# Users
@admin_bp.route(routes["admin"]["users"], methods=['GET', 'POST'])
@login_required
def users(current_user):
  # Variables that the template will use to render
  data = { 'logout_route': '/auth' + routes["auth"]["logout"] }
  return render_template('users.html', data=data)
