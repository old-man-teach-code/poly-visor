from controllers.routes import app_routes
from controllers.api import app_api
from flask_cors import CORS
from flask import Flask
from controllers.utils import check_logs_folder
check_logs_folder()


app = Flask(__name__)
CORS(app)
app.register_blueprint(app_api)
app.register_blueprint(app_routes)

if __name__ == '__main__':
    app.run(threaded=True)
