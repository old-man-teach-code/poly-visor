
from controllers.processes import start_processes
from controllers.supervisor import get_supervisor
from controllers.system import get_system
from flask import Flask,jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='storage/logs/routes.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# restart supervisor
try:
    @app.route('/supervisor/restart', methods=['GET'])
    def restart_supervisor():
        supervisor = get_supervisor()
        supervisor.restart()
        return jsonify({'message': 'Supervisor restarted successfully'})
except Exception as e:
    logger.exception(e)

# shutdown supervisor
try:
    @app.route('/supervisor/shutdown', methods=['GET'])
    def shutdown_supervisor():
        supervisor = get_supervisor()
        supervisor.shutdown()
        return jsonify({'message': 'Supervisor shutdown successfully'})
except Exception as e:
    logger.exception(e)


# start all processes
try:
    @app.route('/processes/start', methods=['GET'])
    def start_processes():
        start_processes()
        return jsonify({'message': 'All processes started successfully'})
except Exception as e:
    logger.exception(e)
