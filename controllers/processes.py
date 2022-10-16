
from models.modelProcess import Process, startAllProcesses

#get all processes
def get_all_processes():
    return Process.getAllProcessInfo()

# start all processes
def start_processes():
    startAllProcesses()
    