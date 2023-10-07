
import json
from time import sleep

from flask_cors import CORS
from flask_jwt_extended import create_access_token
from polyvisor import app
from polyvisor.controllers.utils import is_login_valid, login_required
from polyvisor.controllers.processes import restart_processes_by_name_model, start_processes_by_name_model, stop_all_processes_model, tail_stdErr_logFile_model, tail_stdOut_logFile_model, set_Process_Core_Index, start_all_processes_model, start_process_group_model, stop_process_group_model, stop_processes_by_name_model
from polyvisor.controllers.supervisor import createConfig, restart_supervisor_model, restartSupervisors, shutdown_supervisor_model, shutdownSupervisors
from flask import  jsonify, Blueprint, Response, request, send_from_directory, session
import base64


import logging
from polyvisor.finder import configPolyvisorPath

from polyvisor.models.modelPolyvisor import PolyVisor

app_routes = Blueprint('app_routes', __name__)

app_routes.polyvisor = PolyVisor({"config_file": configPolyvisorPath()})

logger_routes = logging.getLogger(__name__)

CORS(app_routes)


@app_routes.route("/")
def index():
    # return render_template('./build',"index.html")
    return send_from_directory('./build', "index.html")


@app_routes.route("/processes")
def proc():
    # return render_template('./build',"index.html")
    return send_from_directory('./build', "processes.html")


@app_routes.route("/<path:path>")
def base(path):
    return send_from_directory('./build', path)


# # restart supervisor
# try:
#     @app_routes.route('/api/supervisor/restart', methods=['GET'])
#     def restart_supervisor():
#         flag = restart_supervisor_model()
#         if flag:
#             return jsonify({'message': 'Supervisor restarted'})
#         else:
#             return jsonify({'message': 'Supervisor not restarted'})

# except Exception as e:
#     app_routes.logger_routes.debug(e)

# # shutdown supervisor
# try:
#     @app_routes.route('/api/supervisor/shutdown', methods=['GET'])
#     def shutdown_supervisor():
#         flag = shutdown_supervisor_model()
#         if flag:
#             return jsonify({'message': 'Supervisor shutdown successfully'})
#         else:
#             return jsonify({'message': 'Supervisor not shutdown'})

# except Exception as e:
#     app_routes.logger_routes.debug(e)


# # start all processes
# try:
#     @app_routes.route('/api/processes/start', methods=['GET'])
#     def start_processes():
#         flag = start_all_processes_model()
#         if flag:
#             return jsonify({'message': 'All processes started successfully'})
#         else:
#             return jsonify({'message': 'All processes not started'})

# except Exception as e:
#     app_routes.logger_routes.debug(e)

#  start process by name
# try:
#     @app_routes.route('/api/process/start/<name>', methods=['GET'])
#     def start_process_by_name(name):
#         flag = start_process_by_name_model(name)
#         if flag:
#             return jsonify({'message': 'Process started successfully'})
#         else:
#             return jsonify({'message': 'Process not started'})
# except Exception as e:
#     app_routes.logger_routes.debug(e)


# # stop all processes
# try:
#     @app_routes.route('/api/processes/stop', methods=['GET'])
#     @login_required()
#     def stop_processes():
#         flag = stop_all_processes_model()
#         if flag:
#             return jsonify({'message': 'All processes stopped successfully'})
#         else:
#             return jsonify({'message': 'All processes not stopped'})
# except Exception as e:
#     app_routes.logger_routes.debug(e)


# stop process by name
# try:
#     @app_routes.route('/api/process/stop/<name>', methods=['GET'])
#     def stop_process_by_name(name):
#         flag = stop_process_by_name_model(name)
#         if flag:
#             return jsonify({'message': 'Process stopped successfully'})
#         else:
#             return jsonify({'message': 'Process not stopped'})
# except Exception as e:
#     app_routes.logger_routes.debug(e)


# start process group
try:
    @app_routes.route('/api/processes/start/group/<group>', methods=['GET'])
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
    @app_routes.route('/api/processes/stop/group/<group>', methods=['GET'])
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
    @app_routes.route('/api/config/create/<process_name>/<command>', methods=['GET'])
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
    @app_routes.route('/api/config/modify/<process_name>/<action>/<key>/', defaults={'value': ''}, methods=['GET'])
    @app_routes.route('/api/config/modify/<process_name>/<action>/<key>/<value>', methods=['GET'])
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
# try:
#     @app_routes.route('/process/<stream>/<name>', methods=['GET'])
#     def stream(stream, name):
#         def generate():
#             config_path = split_config_path() + name + ".ini"
#             log_path = get_std_log_path(config_path, stream, name)
#             # reading the log file from the end
#             with open(log_path, 'r') as f:
#                 f.seek(0, 2)
#                 while True:
#                     line = f.readline()
#                     if not line:
#                         sleep(1)
#                         continue
#                     message = json.dumps(dict(message=line))
#                     yield "data: {}\n\n".format(message)

#         return Response(generate(), mimetype='text/event-stream')
# except Exception as e:
#     app_routes.logger_routes.debug(e)

try:
    @app_routes.route('/api/process/<stream>/<uid>', methods=['GET'])
    def process_log_tail(stream, uid):
        sname, pname = uid.split(":", 1)
        polyvisor = PolyVisor({"config_file": configPolyvisorPath()})
        supervisor = polyvisor.get_supervisor(sname)
        server = supervisor.server.supervisor

        if stream == "out":
            tail = server.tailProcessStdoutLog
        else:
            tail = server.tailProcessStderrLog

        def event_stream():
            i, offset, length = 0, 0, 2 ** 12
            while True:
                data = tail(pname, offset, length)
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





# create the config file by using POST method
try:
    @app_routes.route('/api/config/create', methods=['POST'])
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
        edit = data['edit']

        result = createConfig(
            process_full_name=process_full_name,
            command=command,
            numprocs=numprocs,
            umask=umask,
            numprocs_start=numprocs_start,
            priority=priority,
            autostart=autostart,
            autorestart=autorestart,
            startsecs=startsecs,
            startretries=startretries,
            exitcodes=exitcodes,
            stopsignal=stopsignal,
            stopwaitsecs=stopwaitsecs,
            stopasgroup=stopasgroup,
            killasgroup=killasgroup,
            redirect_stderr=redirect_stderr,
            stdout_logfile_maxbytes=stdout_logfile_maxbytes,
            stdout_logfile_backups=stdout_logfile_backups,
            stdout_capture_maxbytes=stdout_capture_maxbytes,
            stdout_events_enabled=stdout_events_enabled,
            stdout_syslog=stdout_syslog,
            stderr_logfile_maxbytes=stderr_logfile_maxbytes,
            stderr_logfile_backups=stderr_logfile_backups,
            stderr_capture_maxbytes=stderr_capture_maxbytes,
            stderr_events_enabled=stderr_events_enabled,
            stderr_syslog=stderr_syslog,
            environment=environment,
            serverurl=serverurl,
            directory=directory)
        if (result):
            if (edit):
                return jsonify({'message': 'Config file updated successfully'})
            else:
                return jsonify({'message': 'Config file created successfully'})
        else:
            if (edit):
                return jsonify({'message': 'Config file update failed'})
            else:
                return jsonify({'message': 'Config file creation failed'})
except Exception as e:
    app_routes.logger_routes.debug(e)

# Set affinity list in CPU
try:
    @app_routes.route('/api/cpu/set_affinity/<pid>/<core_index>', methods=['GET'])
    def set_process_core_index_route(pid, core_index):
        result = set_Process_Core_Index(pid, core_index)
        return jsonify({'result': result})
except Exception as e:
    app_routes.logger_routes.debug(e)

# logout of the session
try:
    @app_routes.route("/api/logout", methods=["POST"])
    def logout():
        session.clear()
        return jsonify({"message": "logged out"})
except Exception as e:
    app_routes.logger_routes.debug(e)

# login to the application
try:
    @app_routes.route("/api/login", methods=["POST"])
    def login():

        if not app_routes.polyvisor.use_authentication:
            return "Authentication is not required"
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        supervisor_name = data["supervisor_name"]

        if app_routes.polyvisor.is_user_authorized(supervisor_name, username, password):
            access_token = create_access_token(identity=username)
            session["logged_in"] = True
            session["username"] = username
            return jsonify(access_token=access_token)
        else:
            return jsonify({"message": "Invalid username or password"}), 401
except Exception as e:
    app_routes.logger_routes.debug(e)



# get supervisor


#stop supervisord instance by uid
try:
    @app_routes.route('/api/supervisors/shutdown', methods=['POST'])
    
    def shutdown_supervisor_api():
        names = (
            str.strip(supervisor) for supervisor in request.form["supervisor"].split(",")
        )
        result = shutdownSupervisors(*names)
        if(result):
            return jsonify({'message': 'Supervisor shutdown successfully'})
        else:
            return jsonify({'message': 'Supervisor not shutdown'})
except Exception as e:
    app_routes.logger_api.debug(e)    

# restart supervisord instance by names
try:
    @app_routes.route('/api/supervisors/restart', methods=['POST'])
    @login_required(app_routes, supervisor_name=request.form["supervisor"])
    def restart_supervisor_api():
        names = (
            str.strip(supervisor) for supervisor in request.form["supervisor"].split(",")
        )
        result = restartSupervisors(*names)
        return jsonify(result)
    
except Exception as e:
    app_routes.logger_api.debug(e)    

# stop process by names
try:
    @app_routes.route('/api/processes/stop', methods=['POST'])
    def stop_process_by_name_api():
        names = request.form["uid"].split(",")
        result = stop_processes_by_name_model(*names)
        return jsonify(result)

except Exception as e:
    app_routes.logger_api.debug(e)


# restart process by names
try:
    @app_routes.route('/api/processes/restart', methods=['POST'])
    def restart_process_by_name_api():
        names = request.form["uid"].split(",")
        result = restart_processes_by_name_model(*names)
        return jsonify(result)
    
except Exception as e:
    app_routes.logger_api.debug(e)

# start process by names
try:
    @app_routes.route('/api/processes/start', methods=['POST'])
    def start_process_by_name_api():
        names = request.form["uid"].split(",")
        result =start_processes_by_name_model(*names)
        return jsonify(result)
except Exception as e:
    app_routes.logger_api.debug(e)

# stop all processes
try:
    @app_routes.route('/api/processes/stop', methods=['GET'])
    def stop_all_processes_api():
        result = stop_all_processes_model()
        return jsonify(result)
except Exception as e:
    app_routes.logger_api.debug(e)

# start all processes
try:
    @app_routes.route('/api/processes/start', methods=['GET'])
    def start_all_processes_api():
        result = start_all_processes_model()
        return jsonify(result)
except Exception as e:
    app_routes.logger_api.debug(e)