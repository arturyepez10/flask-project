# import the Flask class from the flask module
from flask import Flask, render_template

# import routes
from controllers.routes import routes

# test to try to separate controllers from app.py
from controllers.auth import auth_bp

# create the application object
app = Flask(__name__)

# ------------------------ ROUTES && BLUEPRINTS ----------------------------- #
# Homepage
@app.route('/')
def home():
    # Variables that the template will use to render
    data = { 'login_route': '/auth' + routes["auth"]["login"] }
    return render_template('home.html', data=data)

# Auth Module
app.register_blueprint(auth_bp, url_prefix='/auth')

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)