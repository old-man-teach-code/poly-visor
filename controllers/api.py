from controllers.processes import get_all_processes_model
from controllers.supervisor import get_supervisor
from controllers.system import get_system
from controllers.utils import get_date
from flask import jsonify, Blueprint
import logging

app_api = Blueprint('app_api', __name__)

# log exception to storage/logs/date/api.log with the date of today
logging.basicConfig(filename='storage/logs/'+get_date()+'/api.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s', force=True)
logger=logging.getLogger(__name__)

#get all processes and return a json object
try:
    @app_api.route('/api/processes', methods=['GET'])
    def get_all_processes_api():
        list_of_processes = get_all_processes_model()
        list_of_processes_json = []
        for process in list_of_processes:
            list_of_processes_json.append(process.__dict__)
        return jsonify(list_of_processes_json)
except Exception as e:
    logger.exception(e)

#get supervisor object and return a json object
try:
    @app_api.route('/api/supervisor', methods=['GET'])
    def get_supervisor_api():
        supervisor = get_supervisor()
        return jsonify({'stateName':supervisor.stateName,'stateCode':supervisor.stateCode, 'pid':supervisor.pid})
except Exception as e:
    logger.exception(e)     


#get system object and return a json object
try:
    @app_api.route('/api/system', methods=['GET'])
    def get_system_api():
        system = get_system()
        return jsonify({'cpu': system.current_cpu_usage,'cores':system.each_cpu_usage, 'memory':system.memory_status, 'machineSpec':system.machine_spec})
except Exception as e:
    #logging the exception to a test.log file in the storage/logs folder
    logger.exception(e)
    
