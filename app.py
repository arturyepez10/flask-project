# ------------------------ IMPORTS ----------------------------- #
# Libraries
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Locals
from database import db, create_tables
from controllers.routes import routes
from controllers.auth import auth_bp

# ------------------------ INITIALIZATION ----------------------------- #
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SECRET_KEY'] = 'super-secret'

    register_extensions(app)
    register_routes(app)
    register_blueprints(app)
    return app

def register_extensions(app: Flask):
    db.init_app(app)
    app.before_first_request(create_tables)

    return None

# ------------------------ ROUTES && BLUEPRINTS ----------------------------- #
def register_routes(app: Flask):
    # Homepage
    @app.route('/')
    def home():
        # Variables that the template will use to render
        data = { 'login_route': '/auth' + routes["auth"]["login"] }
        return render_template('home.html', data=data)

def register_blueprints(app: Flask):
    # Auth Module
    app.register_blueprint(auth_bp, url_prefix='/auth')
