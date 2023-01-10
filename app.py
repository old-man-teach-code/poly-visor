from controllers.utils import check_logs_folder
check_logs_folder()
from flask import Flask
from flask_cors import CORS
from controllers.api import app_api
from controllers.routes import app_routes



app = Flask(__name__)
CORS(app)
app.register_blueprint(app_api)
app.register_blueprint(app_routes)

