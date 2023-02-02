<<<<<<< HEAD
from controllers.routes import app_routes
from controllers.api import app_api
from flask_cors import CORS
from flask import Flask
from controllers.utils import check_logs_folder
check_logs_folder()
=======
from polyvisor.controllers.utils import check_logs_folder
check_logs_folder()
from flask import Flask
from flask_cors import CORS
from polyvisor.controllers.api import app_api
from polyvisor.controllers.routes import app_routes

>>>>>>> 7f34956d7136ed484ce55dd2593dbb9a083c7f16


app = Flask(__name__,static_folder="./build")
CORS(app)
app.register_blueprint(app_api)
app.register_blueprint(app_routes)

if __name__ == '__main__':
    app.run(threaded=True)
