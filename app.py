# ------------------------ IMPORTS ----------------------------- #
# Libraries
from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

# Locals
from database import db, create_tables
from controllers.auth import auth_bp

# ------------------------ INITIALIZATION ----------------------------- #
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SECRET_KEY'] = 'super-secret'

    register_extensions(app)
    register_routes(app)
    register_blueprints(app)
    register_errors_handlers(app)
    return app

def register_extensions(app: Flask):
    db.init_app(app)
    app.before_first_request(create_tables)

    return None

# ------------------------ ROUTES, BLUEPRINTS && ERROR HANDLERS ----------------------------- #
def register_routes(app: Flask):
    # Homepage
    @app.route('/')
    def home():
        return redirect('/auth/login')

def register_blueprints(app: Flask):
    # Auth Module
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
def register_errors_handlers(app: Flask):
    # Custom actions when a 401 is detected in Flask
    @app.errorhandler(401)
    def custom_401(error):
        print(error)
        return redirect('/')