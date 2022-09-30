
from flask import Flask, render_template, Response, request, json, jsonify, session
from sup_information import get_current_cpu_usage, get_each_cpu_usage, get_hostname, get_memory_status, process_PID, process_readLogFile_out, process_swap, sup_Identification, sup_State, process_AllInfo, process_memory_usage, process_Info
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# get the state of the supervisor
@app.route('/api/state')
def returnState():
    return jsonify((sup_State()))


# get all process info
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


# get the swap memory used by the process
@app.route('/api/processSwap/<pid>')
def returnProcessSwap(pid):
    result = process_swap(pid)
    # remove "kb" at the end of the string
    result = result.replace("kB", "")
    # convert the result to json with the format {"key": "value"}
    result = (dict([line.split() for line in result.splitlines()]))
    return jsonify(result)


# get host name
@app.route('/api/hostname')
def returnHostname():
    # return the result with the format {"Host name": "value"}
    result = get_hostname()
    result = result.replace("\n", "")
    return jsonify({"Host name": result})


# get identifications
@app.route('/api/identifications')
def returnIdentifications():
    result = sup_Identification()
    return jsonify(result)


# get PID by name
@app.route('/api/pid/<name>')
def returnPid(name):
    result = process_PID(name)
    return jsonify({name: result})


# get current cpu usage
@app.route('/api/cpuUsage')
def returnCpuUsage():
    result = get_current_cpu_usage()
    result = result.replace("%\n", "")
    return jsonify({"cpuUsage": result})


# get each core cpu usage
@app.route('/api/cpuUsageCore')
def returnCpuCoreUsage():
    result = get_each_cpu_usage()
    result = result.replace("\nst", "")
    result = result.replace("\n", " ")
    result = result.replace("us,", "")
    result = result.replace(":", " ")
    result = dict(zip(result.split()[::2], result.split()[1::2]))
    return result


# get memory status
@app.route('/api/memoryStatus')
def returnMemoryStatus():
    result = get_memory_status()
    result = result.replace("\n", "")
    return jsonify({"Memory": result})

