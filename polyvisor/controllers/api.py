from flask_cors import CORS
from flask_jwt_extended import jwt_required

from polyvisor.controllers.processes import get_all_processes_model, process_Core_Index
from polyvisor.controllers.supervisor import get_config_info, get_supervisor, getMultipleSupervisors, getSupervisor, getSupervisorProcesses, renderConfig
from polyvisor.controllers.system import get_system
from polyvisor.controllers.utils import login_required
from flask import jsonify, Blueprint
from polyvisor.models.modelPolyvisor import PolyVisor
import logging

app_api = Blueprint('app_api', __name__)

CORS(app_api)



# configure logger again for api after routes logger
logger_api = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

# # get all processes and return a json object
# try:
#     @app_api.route('/api/processes', methods=['GET'])
#     def get_all_processes_api():
#         list_of_processes = get_all_processes_model()
#         list_of_processes_json = []
#         for process in list_of_processes:
#             list_of_processes_json.append(process.__dict__)
#         return jsonify(list_of_processes_json)
# except Exception as e:
#     logger_api.debug(e)

# # get supervisor object and return a json object
# try:
#     @app_api.route('/api/supervisor', methods=['GET'])
    
    
#     def get_supervisor_api():
#         supervisor = get_supervisor()
#         # print the session variable
        
#         return jsonify({'stateName': supervisor.stateName, 'stateCode': supervisor.stateCode, 'pid': supervisor.pid})
# except Exception as e:
#     logger_api.debug(e)


# get system object and return a json object
try:
    @app_api.route('/api/system', methods=['GET'])
    def get_system_api():
        system = get_system()
        return jsonify({'cpu': system.current_cpu_usage, 'cores': system.each_cpu_usage, 'memory': system.memory_status, 'machineSpec': system.machine_spec})
except Exception as e:
    # logging the exception to a test.log file in the storage/logs folder
    logger_api.debug(e)

# render the config file
try:
    @app_api.route('/api/config/render/<pid>/<uid>', methods=['GET'])
    def render_config(pid, uid):
        process_name = uid.split(":")[1] if len(uid.split(":")) >= 3 else None

        result = renderConfig(process_name, pid)

        return jsonify(result)
except Exception as e:
    logger_api.debug(e)


# render config
try:
    @app_api.route('/api/config/render', methods=['GET'])
    def render_all_config():
        result = get_config_info()
        return jsonify(result)
except Exception as e:
    logger_api.debug(e)

# View current affinity list in CPU
try:
    @app_api.route('/api/affinity/<pid>', methods=['GET'])
    def process_Core_Index_api(pid):
        result = process_Core_Index(pid)
        return jsonify({'core_index': result})
except Exception as e:
    logger_api.debug(e)


# get multiple supervisords
try:
    @app_api.route('/api/supervisors', methods=['GET'])
    def get_supervisors_api():
        supervisor = getMultipleSupervisors()
        return jsonify(supervisor)
except Exception as e:
    logger_api.debug(e)


# get supervisord instance by uid
try:
    @app_api.route('/api/supervisor/<uid>', methods=['GET'])
    def get_supervisor_by_uid_api(uid):
        supervisor = getSupervisor(uid)
        return jsonify(supervisor)
except Exception as e:
    logger_api.debug(e)

# get supervisord processes by uid
try:
    @app_api.route('/api/supervisor/<uid>/processes', methods=['GET'])
    # @jwt_required( )
    def get_supervisor_processes_by_uid_api(uid):
        supervisor = getSupervisorProcesses(uid)
        return jsonify(supervisor)
except Exception as e:
    logger_api.debug(e)
    
