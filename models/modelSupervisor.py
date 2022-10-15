
import sys
from finder import get_sup_serverurl

from models.modelSystem import runShell
from xmlrpc.client import ServerProxy
import re
import configparser 
from collections import OrderedDict

#To get multiple value in config file
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

#Get pid supervisord by name in linux with shell 
def get_pid():
    output=runShell("pgrep supervisord")
    result =output.replace("\n","")
    return result

def config_Path():
    result = runShell("ps -p "+str(get_pid())+" -o args")
    path=""
    s = re.findall(r'(\/.*?\.[\w:]+)', result)
    try:
        lis = s[1].split()
        for x in lis:
            if(r".conf"in x or r".ini" in x):
                path+=x
    except: 
        lis2 = s[0].split()
        for x in lis2:
            if(r".conf"in x or r".ini" in x):
                path+=x

    if path=="" or not path:
        path="Can't find config path of Supervisord"        
    return path




server = ServerProxy("http://localhost"+str(get_sup_serverurl())+"/RPC2")

#server = ServerProxy("http://localhost:9001/RPC2")

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
