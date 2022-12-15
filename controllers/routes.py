
import json
from time import sleep

from flask_cors import CORS
from controllers.processes import clear_all_process_log_model, clear_process_log_model, start_all_processes_model, start_process_by_name_model, start_process_group_model, stop_all_processes_model, stop_process_by_name_model, stop_process_group_model, tail_stdErr_logFile_model, tail_stdOut_logFile_model
from controllers.supervisor import createConfig, modifyConfig, renderConfig, restart_supervisor_model, shutdown_supervisor_model
from flask import jsonify, Blueprint, Response
import base64


import logging

app_routes = Blueprint('app_routes', __name__)

logger_routes = logging.getLogger(__name__)

CORS(app_routes)

# restart supervisor
try:
    @app_routes.route('/supervisor/restart', methods=['GET'])
    def restart_supervisor():
        flag = restart_supervisor_model()
        if flag:
            return jsonify({'message': 'Supervisor restarted'})
        else:
            return jsonify({'message': 'Supervisor not restarted'})    
            
except Exception as e:
    app_routes.logger_routes.debug(e)

# shutdown supervisor
try:
    @app_routes.route('/supervisor/shutdown', methods=['GET'])
    def shutdown_supervisor():
        flag = shutdown_supervisor_model()
        if flag:
            return jsonify({'message': 'Supervisor shutdown successfully'})
        else:
            return jsonify({'message': 'Supervisor not shutdown'})    
            
except Exception as e:
    app_routes.logger_routes.debug(e)


# start all processes
try:
    @app_routes.route('/processes/start', methods=['GET'])
    def start_processes():
        flag = start_all_processes_model()
        if flag:
            return jsonify({'message': 'All processes started successfully'})
        else:    
            return jsonify({'message': 'All processes not started'})

except Exception as e:
    app_routes.logger_routes.debug(e)

#  start process by name
try:
    @app_routes.route('/process/start/<name>', methods=['GET'])
    def start_process_by_name(name):
        flag = start_process_by_name_model(name)
        if flag:
            return jsonify({'message': 'Process started successfully'})
        else:
            return jsonify({'message': 'Process not started'})
except Exception as e:
    app_routes.logger_routes.debug(e)


# stop all processes
try:
    @app_routes.route('/processes/stop', methods=['GET'])
    def stop_processes():
        flag = stop_all_processes_model()
        if flag:
            return jsonify({'message': 'All processes stopped successfully'})
        else:
            return jsonify({'message': 'All processes not stopped'})
except Exception as e:
    app_routes.logger_routes.debug(e)


# stop process by name
try:
    @app_routes.route('/process/stop/<name>', methods=['GET'])
    def stop_process_by_name(name):
        flag = stop_process_by_name_model(name)
        if flag:
            return jsonify({'message': 'Process stopped successfully'})
        else:
            return jsonify({'message': 'Process not stopped'})
except Exception as e:
    app_routes.logger_routes.debug(e)


# start process group
try:
    @app_routes.route('/processes/start/group/<group>', methods=['GET'])
    def start_process_group(group):
        flag = start_process_group_model(group)
        if flag:
            return jsonify({'message': 'Process group started successfully'})
        else:
            return jsonify({'message': 'Process group not started'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# stop process group
try:
    @app_routes.route('/processes/stop/group/<group>', methods=['GET'])
    def stop_process_group(group):
        flag = stop_process_group_model(group)
        if flag:
            return jsonify({'message': 'Process group stopped successfully'})
        else:
            return jsonify({'message': 'Process group not stopped'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# tail stdOut and stdErr log file
try:
    @app_routes.route('/process/<stream>/<name>', methods=['GET'])
    def process_log_tail(stream, name):
        if stream == "out":
            tail = tail_stdOut_logFile_model
        else:
            tail = tail_stdErr_logFile_model

        def event_stream():
            i, offset, length = 0, 0, 2 ** 12
            while True:
                data = tail(name, offset, length)
                log, offset, overflow = data
                # don't care about overflow in first log message
                if overflow and i:
                    length = min(length * 2, 2 ** 14)
                else:
                    data = json.dumps(dict(message=log, size=offset))
                    yield "data: {}\n\n".format(data)
                sleep(1)
                i += 1

        return Response(event_stream(), mimetype="text/event-stream")
except Exception as e:
    app_routes.logger_routes.debug(e)

# make the route to create config file
try:
    @app_routes.route('/config/create/<process_name>/<command>', methods=['GET'])
    def create_config(process_name, command):
        
        command = base64.b64decode(command).decode('utf-8')
        result = createConfig(process_name, command)
        if (result):
            return jsonify({'message': 'Config file created successfully'})
        else:
            return jsonify({'message': 'Config file creation failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# update the config file
try:
    @app_routes.route('/config/modify/<process_name>/<action>/<key>/',defaults={'value': ''}, methods=['GET'] )
    @app_routes.route('/config/modify/<process_name>/<action>/<key>/<value>', methods=['GET'])
    def modify_config(process_name, action, key, value):
        value = base64.b64decode(value).decode('utf-8')
        result = modifyConfig(process_name, action, key, value)
        if (result):
            return jsonify({'message': 'Config file updated successfully'})
        else:
            return jsonify({'message': 'Config file update failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# render the config file
try:
    @app_routes.route('/config/render/<process_name>', methods=['GET'])
    def render_config(process_name):
        result = renderConfig(process_name)
        if (result):
            return jsonify({'message': 'Config file rendered successfully'})
        else:
            return jsonify({'message': 'Config file render failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# clear process log with name
try:
    @app_routes.route('/process/log/clear/<name>', methods=['GET'])
    def clear_process_log(name):
        result = clear_process_log_model(name)
        if (result):
            return jsonify({'message': 'Process log cleared successfully'})
        else:
            return jsonify({'message': 'Process log clear failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# clear all process logs
try:
    @app_routes.route('/processes/log/clearAll', methods=['GET'])
    def clear_all_process_logs():
        result = clear_all_process_log_model()
        if (result):
            return jsonify({'message': 'All process logs cleared successfully'})
        else:
            return jsonify({'message': 'All process logs clear failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)