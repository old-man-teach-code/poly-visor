
import json
from time import sleep
from controllers.processes import start_all_processes_model, start_process_by_name_model, start_process_group_model, stop_all_processes_model, stop_process_by_name_model, stop_process_group_model, tail_stdErr_logFile_model, tail_stdOut_logFile_model
from controllers.supervisor import createConfig, modifyConfig, restart_supervisor_model, shutdown_supervisor_model
from flask import jsonify, Blueprint, Response

import logging

app_routes = Blueprint('app_routes', __name__)

logger_routes = logging.getLogger(__name__)


# restart supervisor
try:
    @app_routes.route('/supervisor/restart', methods=['GET'])
    def restart_supervisor():
        restart_supervisor_model()
        return jsonify({'message': 'Supervisor restarted'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# shutdown supervisor
try:
    @app_routes.route('/supervisor/shutdown', methods=['GET'])
    def shutdown_supervisor():
        shutdown_supervisor_model()
        return jsonify({'message': 'Supervisor shutdown successfully'})
except Exception as e:
    app_routes.logger_routes.debug(e)


# start all processes
try:
    @app_routes.route('/processes/start', methods=['GET'])
    def start_processes():
        start_all_processes_model()
        return jsonify({'message': 'All processes started successfully'})
except Exception as e:
    app_routes.logger_routes.debug(e)

#  start process by name
try:
    @app_routes.route('/processes/start/<name>', methods=['GET'])
    def start_process_by_name(name):
        start_process_by_name_model(name)
        return jsonify({'message': 'Process started successfully'})
except Exception as e:
    app_routes.logger_routes.debug(e)


# stop all processes
try:
    @app_routes.route('/processes/stop', methods=['GET'])
    def stop_processes():
        stop_all_processes_model()
        return jsonify({'message': 'All processes stopped successfully'})
except Exception as e:
    app_routes.logger_routes.debug(e)


# stop process by name
try:
    @app_routes.route('/processes/stop/<name>', methods=['GET'])
    def stop_process_by_name(name):
        stop_process_by_name_model(name)
        return jsonify({'message': 'Process stopped successfully'})
except Exception as e:
    app_routes.logger_routes.debug(e)


# start process group
try:
    @app_routes.route('/processes/start/group/<group>', methods=['GET'])
    def start_process_group(group):
        start_process_group_model(group)
        return jsonify({'message': 'Process group started successfully'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# stop process group
try:
    @app_routes.route('/processes/stop/group/<group>', methods=['GET'])
    def stop_process_group(group):
        stop_process_group_model(group)
        return jsonify({'message': 'Process group stopped successfully'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# tail stdOut and stdErr log file
try:
    @app_routes.route('/processes/<stream>/<name>', methods=['GET'])
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
        result = modifyConfig(process_name, action, key, value)
        if (result):
            return jsonify({'message': 'Config file updated successfully'})
        else:
            return jsonify({'message': 'Config file update failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)
