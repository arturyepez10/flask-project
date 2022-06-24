# ------------------------ IMPORTS ----------------------------- #
# Libraries
from flask import Flask, redirect

# Locals
from database import db, create_tables
from controllers.auth import auth_bp
from controllers.admin import admin_bp

# ------------------------ INITIALIZATION ----------------------------- #
def create_app(type = 'dev'):
  app = Flask(__name__)
  
  if type == 'test':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_tests.sqlite'
    app.config['TESTING'] = True
  else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

  app.config['SECRET_KEY'] = 'super-secret'
  print(app.config['SQLALCHEMY_DATABASE_URI'])

  register_extensions(app, type == 'test')
  register_routes(app)
  register_blueprints(app)
  register_errors_handlers(app)
  return app

def register_extensions(app: Flask, testing = False):
  db.init_app(app)
  app.before_first_request(lambda : create_tables(testing))
    
# ------------------------ ROUTES, BLUEPRINTS && ERROR HANDLERS ----------------------------- #
def register_routes(app: Flask):
  # Homepage
  @app.route('/')
  def home():
    return redirect('/auth/login')

def register_blueprints(app: Flask):
  # Auth Module
  app.register_blueprint(auth_bp, url_prefix='/auth')

  # Admin Module
  app.register_blueprint(admin_bp, url_prefix='/admin')
  
def register_errors_handlers(app: Flask):
  # Custom actions when a 401 is detected in Flask
  @app.errorhandler(401)
  def custom_401(error):
    print(error)
    return redirect('/')