import sys
import os
# Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
from models.modelProcess import Process, allData_stdErr_logFile, allData_stdOut_logFile, startAllProcesses, startProcessByName, stopAllProcesses, stopProcessByName, clear_process_log

#get all processes info
def get_all_processes_model():
    return Process.getAllProcessInfo()

#start all processes, return array result
def start_all_processes_model():
    return startAllProcesses()    

#start process by name, always return True unless error
def start_process_by_name_model(name):
    return startProcessByName(name)

#stop process by name, always return True unless error
def stop_process_by_name_model(name):
    return stopProcessByName(name)

#stop ALL process, return array result
def stop_all_processes_model():
    return stopAllProcesses()

#get all data StdOut  of process by name
def get_all_stdOut_process_model(name):
    return allData_stdOut_logFile(name)

#get all data StdErr  of process by name
def get_all_stdErr_process_model(name):
    return allData_stdErr_logFile(name)

# clear stdOut, stdErr of process by name
def clear_log_process_by_name_model(name):
    return clear_process_log(name)
print(get_all_stdOut_process_model("Demo0"))