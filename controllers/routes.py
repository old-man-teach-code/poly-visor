
import json
from time import sleep

from flask_cors import CORS
from finder import get_std_log_path, split_config_path
from controllers.processes import set_Process_Core_Index, start_all_processes_model, start_process_by_name_model, start_process_group_model, stop_all_processes_model, stop_process_by_name_model, stop_process_group_model
from controllers.supervisor import createConfig, restart_supervisor_model, shutdown_supervisor_model
from flask import jsonify, Blueprint, Response, request
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

#
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
    @app_routes.route('/config/modify/<process_name>/<action>/<key>/', defaults={'value': ''}, methods=['GET'])
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



# tail the /var/log/demo.out.log on the browser
try:
    @app_routes.route('/process/<stream>/<name>', methods=['GET'])
    def stream(stream, name):
        def generate():
            config_path = split_config_path() + name + ".ini"
            log_path = get_std_log_path(config_path, stream, name)
            # reading the log file from the end
            with open(log_path, 'r') as f:
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if not line:
                        sleep(1)
                        continue
                    message = json.dumps(dict(message=line))
                    yield "data: {}\n\n".format(message)

        return Response(generate(), mimetype='text/event-stream')
except Exception as e:
    app_routes.logger_routes.debug(e)


# create the config file by using POST method
try:
    @app_routes.route('/config/create', methods=['POST'])
    def create_config_post():
        data = request.get_json()
        process_full_name = data['process_full_name']
        command = data['command']
        numprocs = data['numprocs']
        umask = data['umask']
        numprocs_start = data['numprocs_start']
        priority = data['priority']
        autostart = data['autostart']
        autorestart = data['autorestart']
        startsecs = data['startsecs']
        startretries = data['startretries']
        exitcodes = data['exitcodes']
        stopsignal = data['stopsignal']
        stopwaitsecs = data['stopwaitsecs']
        stopasgroup = data['stopasgroup']
        killasgroup = data['killasgroup']
        redirect_stderr = data['redirect_stderr']
        stdout_logfile_maxbytes = data['stdout_logfile_maxbytes']
        stdout_logfile_backups = data['stdout_logfile_backups']
        stdout_capture_maxbytes = data['stdout_capture_maxbytes']
        stdout_events_enabled = data['stdout_events_enabled']
        stdout_syslog = data['stdout_syslog']
        stderr_logfile_maxbytes = data['stderr_logfile_maxbytes']
        stderr_logfile_backups = data['stderr_logfile_backups']
        stderr_capture_maxbytes = data['stderr_capture_maxbytes']
        stderr_events_enabled = data['stderr_events_enabled']
        stderr_syslog = data['stderr_syslog']
        environment = data['environment']
        serverurl = data['serverurl']
        directory = data['directory']

        result = createConfig(
            process_full_name = process_full_name,
            command = command,
            numprocs = numprocs,
            umask = umask,
            numprocs_start = numprocs_start,
            priority = priority,
            autostart = autostart,
            autorestart = autorestart,
            startsecs = startsecs,
            startretries = startretries,
            exitcodes = exitcodes,
            stopsignal = stopsignal,
            stopwaitsecs = stopwaitsecs,
            stopasgroup = stopasgroup,
            killasgroup = killasgroup,
            redirect_stderr = redirect_stderr,
            stdout_logfile_maxbytes = stdout_logfile_maxbytes,
            stdout_logfile_backups = stdout_logfile_backups,
            stdout_capture_maxbytes = stdout_capture_maxbytes,
            stdout_events_enabled = stdout_events_enabled,
            stdout_syslog = stdout_syslog,
            stderr_logfile_maxbytes = stderr_logfile_maxbytes,
            stderr_logfile_backups = stderr_logfile_backups,
            stderr_capture_maxbytes = stderr_capture_maxbytes,
            stderr_events_enabled = stderr_events_enabled,
            stderr_syslog = stderr_syslog,
            environment = environment,
            serverurl = serverurl,
            directory = directory)
        if (result):
            return jsonify({'message': 'Config file created successfully'})
        else:
            return jsonify({'message': 'Config file creation failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# create update the config file by using POST method
try:
    @app_routes.route('/config/modify', methods=['POST'])
    def modify_config_post():
        data = request.get_json()
        process_name = data['process_name']
        action = data['action']
        key = data['key']
        value = data['value']

        result = modifyConfig(process_name, action, key, value)
        if (result):
            return jsonify({'message': 'Config file updated successfully'})
        else:
            return jsonify({'message': 'Config file update failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# Set affinity list in CPU
try:
    @app_routes.route('/cpu/set_affinity/<pid>/<core_index>', methods=['GET'])
    def set_process_core_index_route(pid, core_index):
        result = set_Process_Core_Index(pid, core_index)
        print(result)
        return jsonify(result)
except Exception as e:
    app_routes.logger_routes.debug(e)