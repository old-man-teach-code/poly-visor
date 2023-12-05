
import json
from gevent import queue, sleep
from blinker import signal




from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required
# from polyvisor import app
from polyvisor.controllers.processes import restart_processes_by_name_model, start_all_processes_by_supervisor_model, start_processes_by_name_model, stop_all_processes_by_supervisor_model, set_Process_Core_Index, start_process_group_model, stop_process_group_model, stop_processes_by_name_model
from polyvisor.controllers.supervisor import createConfig, restartSupervisors, shutdownSupervisors
from flask import  jsonify, Blueprint, Response, make_response, redirect, render_template, request, send_from_directory, session, url_for
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

@app_routes.route("/login")
def login_route():    
    return send_from_directory('./build', "login.html")
    

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
#     logger_routes.debug(e)

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
#     logger_routes.debug(e)


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
#     logger_routes.debug(e)

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
#     logger_routes.debug(e)


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
#     logger_routes.debug(e)


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
#     logger_routes.debug(e)


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
    logger_routes.debug(e)

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
    logger_routes.debug(e)

#

# update the config file


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
#     logger_routes.debug(e)

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
    logger_routes.debug(e)





# create the config file by using POST method
try:
    @app_routes.route('/api/config/create', methods=['POST'])
    def create_config_post():
        data = request.get_json(force=True)
        pid = data['pid']
        supervisor_name = data['supervisor_name']
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
            pid=pid,
            supervisor_name=supervisor_name,
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
     jsonify({'message': 'Config file creation failed'})

# Set affinity list in CPU
try:
    @app_routes.route('/api/cpu/set_affinity/<pid>/<core_index>', methods=['GET'])
    def set_process_core_index_route(pid, core_index):
        result = set_Process_Core_Index(pid, core_index)
        return jsonify({'result': result})
except Exception as e:
    logger_routes.debug(e)


SIGNALS = [
    "process_changed",
    "supervisor_changed",
    "notification",
]


# class Dispatcher(object):
#     def __init__(self):
#         self.clients = []
#         for signal_name in SIGNALS:
#             signal(signal_name).connect(self.on_event)

#     def add_listener(self, client):
#         self.clients.append(client)

#     def remove_listener(self, client):
#         self.clients.remove(client)

#     def on_event(self, signal, payload):
#         data = json.dumps(dict(payload=payload, event=signal))
#         event = "data: {0}\n\n".format(data)
#         for client in self.clients:
#             client.put(event)

# logout of the session
try:
    @app_routes.route("/api/logout", methods=["POST"])
    def logout():
        session.clear()
        response = make_response(jsonify({"status": 200, "data": {"message": "Logout successfully"}}))
        response.set_cookie('access_token_cookie', '', expires=0, secure=True)
        # Include the JSON response in the 'response' object
        return response, 200

except Exception as e:
    logger_routes.debug(e)

# login to the application
from flask import jsonify

@app_routes.route("/api/login", methods=["POST"])
def login():
    try:
        supervisor_name = request.form.get("supervisor")
        username = request.form.get("username")
        password = request.form.get("password")

        # Initialize the response variable
        response = jsonify()

        if not app_routes.polyvisor.use_authentication:
            access_token = create_access_token(identity="guest")
        else:
            if app_routes.polyvisor.is_login_valid(supervisor_name, username, password):
                # Create an access token
                access_token = create_access_token(identity=username)
            else:
                json_response = jsonify({"status": 401, "data": {"message": "Invalid username or password"}})
                response.data = json_response.data
                response.content_type = json_response.content_type
                return response, 401

        # Set the JWT token as an HTTP-only cookie
        response.set_cookie('access_token_cookie', access_token, httponly=True, samesite='Lax', secure=True)

        json_response = jsonify({"status": 200, "data": {"message": "Login successfully"}})

        # Include the JSON response in the 'response' object
        response.data = json_response.data
        response.content_type = json_response.content_type

        return response, 200

    except Exception as e:
        logger_routes.debug(e)



# get supervisor


#stop supervisord instance by uid
try:
    @app_routes.route('/api/supervisors/shutdown', methods=['POST'])
    @jwt_required( )
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
    logger_routes.debug(e)  

# restart supervisord instance by names
try:
    @app_routes.route('/api/supervisors/restart', methods=['POST'])
    @jwt_required( )
    def restart_supervisor_api():
        print("Form: ", request.form["supervisor"])
        names = (
            str.strip(supervisor) for supervisor in request.form["supervisor"].split(",")
        )
        result = restartSupervisors(*names)
        return jsonify(result)
    
except Exception as e:
    
    logger_routes.debug(e)  

# stop process by names
try:
    @app_routes.route('/api/processes/stop', methods=['POST'])
    @jwt_required( )
    def stop_process_by_name_api():
        names = request.form["uid"].split(",")
        result = stop_processes_by_name_model(*names)
        if(result):
            return jsonify({'message': 'Process stopped successfully'})
        else:
            return jsonify({'message': 'Process not stopped'})

except Exception as e:
    logger_routes.debug(e)


# restart process by names
try:
    @app_routes.route('/api/processes/restart', methods=['POST'])
    @jwt_required( )
    def restart_process_by_name_api():
        names = request.form["uid"].split(",")
        result = restart_processes_by_name_model(*names)
        if(result):
            return jsonify({'message': 'Process restarted successfully'})
        else:
            return jsonify({'message': 'Process not restarted'})
    
except Exception as e:
    logger_routes.debug(e)

# start process by names
try:
    @app_routes.route('/api/processes/start', methods=['POST'])
    @jwt_required( )
    def start_process_by_name_api():
        names = request.form["uid"].split(",")
        result =start_processes_by_name_model(*names)
        if(result):
            return jsonify({'message': 'Process started successfully'})
        else:
            return jsonify({'message': 'Process not started'})
except Exception as e:
    logger_routes.debug(e)

# stop all processes
try:
    @app_routes.route('/api/processes/stopAll/<name>', methods=['GET'])
    @jwt_required( )
    def stop_all_processes_api(name):
        result = stop_all_processes_by_supervisor_model(name)
        if(result):
            return jsonify({'message': 'All processes stopped successfully'})
        else:
            return jsonify({'message': 'All processes not stopped'})
except Exception as e:
    logger_routes.debug(e)

# start all processes
try:
    @app_routes.route('/api/processes/startAll/<name>', methods=['GET'])
    @jwt_required( )
    def start_all_processes_api(name):
        result = start_all_processes_by_supervisor_model(name)
        if(result):
            return jsonify({'message': 'All processes started successfully'})
        else:
            return jsonify({'message': 'All processes not started'})
except Exception as e:
    logger_routes.debug(e)



  



 
    