# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import request, make_response, redirect, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists

# ------------------------ INIT ----------------------------- #
db = SQLAlchemy()

def create_tables():
    if not database_exists('sqlite:///db.sqlite'):
        db.create_all()

        default_user = User(username='admin', password='admin', role='admin')
        db.session.add(default_user)
        db.session.commit()

# ------------------------ MODELS ----------------------------- #
# users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# ------------------------ DECORATORS ----------------------------- #
# login decorator
def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # TODO: implementation of jwt
        # token = None
        # user = None
        # if 'x-id' in request.headers and 'x-access-token' in request.headers:
        #     user = User.query.filter_by(id=request.headers['x-id']).first()
        #     if user.password == request.headers['x-access-token']:
        #         token = user.password
        
        # if token is None:
        #     return redirect('/', 401)

        user = None
        if 'username' and 'password' not in session:
            return redirect('/', 401)
        else:
            user = { 'username': session['username'], 'password': session['password'] }

        return f(current_user=user, *args, **kwargs)
    return decorator