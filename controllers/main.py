from flask import Flask
from flask_cors import CORS
from controllers.routes import app_routes
from controllers.api import app_api
app = Flask(__name__)
CORS(app)
app.register_blueprint(app_routes)
app.register_blueprint(app_api)
