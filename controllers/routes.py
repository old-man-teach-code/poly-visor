
from controllers.processes import start_all_processes_model
from controllers.supervisor import get_supervisor, restart_supervisor_model
from controllers.system import get_system
from flask import jsonify, Blueprint
import logging

app_routes = Blueprint('app_routes', __name__)

logging.basicConfig(filename='storage/logs/routes.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# restart supervisor
try:
    @app_routes.route('/supervisor/restart', methods=['GET'])
    def restart_supervisor():
        restart_supervisor_model()
        return jsonify({'message':'Supervisor restarted'})
except Exception as e:
    logger.exception(e)

# shutdown supervisor
try:
    @app_routes.route('/supervisor/shutdown', methods=['GET'])
    def shutdown_supervisor():
        supervisor = get_supervisor()
        supervisor.shutdown()
        return jsonify({'message': 'Supervisor shutdown successfully'})
except Exception as e:
    logger.exception(e)


# start all processes
try:
    @app_routes.route('/processes/start', methods=['GET'])
    def start_processes():
        start_all_processes_model()
        return jsonify({'message': 'All processes started successfully'})
except Exception as e:
    logger.exception(e)
