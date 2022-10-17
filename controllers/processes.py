
from models.modelProcess import Process, startAllProcesses, startProcessByName, stopAllProcesses, stopProcessByName

#get all processes info
def get_allProcesses_model():
    return Process.getAllProcessInfo()

# start all processes, return array result
def start_allProcesses_model():
    return startAllProcesses()    

# start process by name, always return True unless error
def startProcess_byName_model(name):
    return startProcessByName(name)

#stop process by name, always return True unless error
def stopProcess_byName_model(name):
    return stopProcessByName(name)

#stop ALL process, return array result
def stop_allProcesses_model():
    return stopAllProcesses()
