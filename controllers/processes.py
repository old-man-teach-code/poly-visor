
from models.modelProcess import Process, startAllProcesses

#get all processes
def get_all_processes_model():
    return Process.getAllProcessInfo()

# start all processes
def start_all_processes_model():
    startAllProcesses()
    