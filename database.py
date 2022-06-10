# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import make_response, session, abort, request
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists

# ------------------------ INIT ----------------------------- #
db = SQLAlchemy()

def create_tables(testing = False):
    if testing and database_exists('sqlite:///db_tests.sqlite'):
        db.drop_all()

    if not database_exists('sqlite:///db.sqlite') or (testing and database_exists('sqlite:///db_tests.sqlite')):
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
    name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
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
        if 'current_user' not in session or session['current_user'] is None:
            abort(401, 'User unauthorized')
        else:
            user = session['current_user']

        return f(current_user=user, *args, **kwargs)
    # This is a solution for multiple wrappers in similar routes
    decorator.__name__ = f.__name__
    return decorator

# authorize decorator (only for requests)
def authorize_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-token' in request.headers:
            [username, password] = request.headers['x-access-token'].split(' ')
            user = User.query.filter_by(username=username, password=password).first()

            if user is None:
                return make_response('User not found.', 404)
        else:
            abort(401, 'User unauthorized')    
        
        return f(*args, **kwargs)
    return decorator