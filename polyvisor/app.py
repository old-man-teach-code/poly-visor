from datetime import timedelta
from flask_jwt_extended import JWTManager
from polyvisor.controllers.routes import app_routes
from polyvisor.controllers.api import app_api
from flask_cors import CORS
from flask import Flask
from flask_session import Session

app = Flask(__name__, static_folder="./build")
CORS(app)


# Set the session type and key
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
# set the token expiration time
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# Configure JWT for cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api'  # Path to protect with JWT cookies
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  

jwt = JWTManager(app)
# Initialize the session
session = Session(app)


# Register blueprints
app.register_blueprint(app_api)
app.register_blueprint(app_routes)

if __name__ == '__main__':
    app.run(threaded=True)
