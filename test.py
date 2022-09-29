import re
from flask import Flask, render_template, Response, request, json, jsonify, session
from markupsafe import escape
import json
from sup_information import get_hostname, process_swap, sup_State, process_AllInfo,process_memory_usage, process_Info

# ...
import os



app = Flask(__name__)


# get the cpu usage by the os module and assign it to the cpuUsage variable

cpuUsage = os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline()
    

#get the CPU and RAM usage of the system
# ...

@app.route('/capitalize/<word>/')
def capitalize(word):
    return jsonify({'word': word.capitalize()})


@app.route('/api/state')
def returnState():
    return jsonify((sup_State()))

@app.route('/api/allProcessInfo')
def returnAllProcessInfo():
    return jsonify((process_AllInfo()))

# get process info by name
@app.route('/api/processInfo/<name>')
def returnProcessInfo(name):
    return jsonify((process_Info(name)))

# get process_memory_usage
@app.route('/api/processMemoryUsage/<pid>')
def returnProcessMemoryUsage(pid):
    result = process_memory_usage(pid)
    array_result = [line.split() for line in result.splitlines()]
    array_result = list(zip(*array_result))
    return jsonify(dict(array_result))

# get hostname
@app.route('/api/hostname')
def returnHostname():
    return jsonify(get_hostname())

# get the swap memory used by the process
@app.route('/api/processSwap/<pid>')
def returnProcessSwap(pid):
    result = process_swap(pid)
    # remove "kb" at the end of the string
    result = result.replace("kB", "")
    # convert the result to json with the format {"key": "value"}
    result = (dict([line.split() for line in result.splitlines()]))
    return jsonify(result)


    