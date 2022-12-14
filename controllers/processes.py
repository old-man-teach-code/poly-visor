import sys
import os
# Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
from models.modelProcess import Process, read_stdErr_logFile, read_stdOut_logFile, startAllProcesses, startProcessByName, startProcessGroup, stopAllProcesses, stopProcessByName, clear_process_log, stopProcessGroup, tail_stdErr_logFile, tail_stdOut_logFile

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

# start group of process by group name, return array result
def start_process_group_model(group):
    return startProcessGroup(group)

# stop group of process by group name, return array result
def stop_process_group_model(group):
    return stopProcessGroup(group)
#get all data StdOut  of process by name
def read_stdOut_process_model(name):
    return read_stdOut_logFile(name)

#get all data StdErr  of process by name
def read_stdErr_process_model(name):
    return read_stdErr_logFile(name)

# clear stdOut, stdErr of process by name
def clear_log_process_by_name_model(name):
    return clear_process_log(name)

# tail stdOut log file of process with name
def tail_stdOut_logFile_model(name, offset, length):
    return tail_stdOut_logFile(name, offset, length)

# tail stdErr log file of process with name
def tail_stdErr_logFile_model(name, offset, length):
    return tail_stdErr_logFile(name, offset, length)

# assign core to process by using taskset
def assign_core_to_process_model(name, core):
    # check core is number
    if not core.isdigit():
        return False
    # get pid
    # check pid is number    
    pid = Process.getProcessPidByName(name)
    if not pid.isdigit():
        return False
    # assign core to process
    command = "taskset -p -c " + core + " " + pid
    os.system(command)
    return True