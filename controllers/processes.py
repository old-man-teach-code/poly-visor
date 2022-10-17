
from models.modelProcess import Process, startAllProcesses, startProcessByName

#get all processes
def get_all_processes_model():
    return Process.getAllProcessInfo()

# start all processes
def start_all_processes_model():
    startAllProcesses()
    

# start process by name
def start_process_by_name_model(name):
    return startProcessByName(name)