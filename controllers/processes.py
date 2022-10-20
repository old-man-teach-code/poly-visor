
from models.modelProcess import Process, startAllProcesses, startProcessByName, startProcessGroup, stopAllProcesses, stopProcessByName, stopProcessGroup, allData_stdErr_logFile, allData_stdOut_logFile, clear_process_log 



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
def get_all_stdOut_process_model(name):
    return allData_stdOut_logFile(name)

#get all data StdErr  of process by name
def get_all_stdErr_process_model(name):
    return allData_stdErr_logFile(name)

# clear stdOut, stdErr of process by name
def clear_log_process_by_name_model(name):
    return clear_process_log(name)
