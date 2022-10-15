
from controllers.processes import get_all_processes
from controllers.supervisor import get_supervisor
from flask import Flask,jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)



#get all processes and return a json object
try:
    @app.route('/api/processes', methods=['GET'])
    def get_all_processes_api():
        list_of_processes = get_all_processes()
        list_of_processes_json = []
        for process in list_of_processes:
            list_of_processes_json.append(process.__dict__)
        return jsonify(list_of_processes_json)
except Exception as e:
    print(e)

#get supervisor object and return a json object
try:
    @app.route('/api/supervisor', methods=['GET'])
    def get_supervisor_api():
        supervisor = get_supervisor()
        return jsonify(supervisor.__dict__)
except Exception as e:
    print(e)        