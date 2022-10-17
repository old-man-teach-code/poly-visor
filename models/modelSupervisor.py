import sys
import os
#Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
#insert into PYTHONPATH
sys.path.insert(1,parent)

from finder import serverURL
from xmlrpc.client import ServerProxy


server = ServerProxy("http://localhost"+str(serverURL())+"/RPC2")

class Supervisor:

    def __init__(self):
        pass       

    @property    
    def stateName(self):
        state = server.supervisor.getState()   
        return  state['statename']

    @property    
    def stateCode(self):
        state = server.supervisor.getState()      
        return state['statecode']
    
    #Get Supervisor PID
    @property
    def pid(self):
        return server.supervisor.getPID()    

    @property
    def restart(self):
        return server.supervisor.restart()

    @property
    def shutdown(self):
        return server.supervisor.shutdown()

    @property
    def clear_log(self):
        return server.supervisor.clearLog()
        


