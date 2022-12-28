from multiprocessing import reduction
from xmlrpc.client import ServerProxy
import sys
import os
# Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
from finder import serverURL

server = ServerProxy("http://localhost"+str(serverURL())+"/RPC2")

class Supervisor:

    def __init__(self):
        pass

    @property
    def stateName(self):
        state = server.supervisor.getState()
        return state['statename']

    @property
    def stateCode(self):
        state = server.supervisor.getState()
        return state['statecode']

    # Get Supervisor PID
    @property
    def pid(self):
        return server.supervisor.getPID()

    # Restart supervisord
    @property
    def restart(self): 
        return server.supervisor.restart()

    @property
    def shutdown(self):
        return server.supervisor.shutdown()
    #Clear log of supervisord
    @property
    def clear_log(self):
        return server.supervisor.clearLog()
    
    # Get all log of supervisord
    @property
    def all_log(self):
        return server.supervisor.readLog(0,0)

    # Reload config file of supervisor,return array result [[added, changed, removed]]
    @property
    def reload_config_model(self):
        return server.supervisor.reloadConfig()

    #Clear all log of process when it running, return array result status info
    @property
    def clear_all_log_processes(self):
        return server.supervisor.clearAllProcessLogs()

    #Update the config for a running process from config file.    
    @property
    def update_config_model(name):
        return server.supervisor.addProcessGroup(name)

    #  get config info of supervisor
    @property
    def get_config_info_model(self):
        return server.supervisor.getAllConfigInfo()