import sys
sys.path.insert(1,"/home/hlk9/Documents/GitHub/poly-visor/models/modelSystem.py")
import modelSystem
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
    output=modelSystem.runShell("pgrep supervisord")
    result =output.replace("\n","")
    return result

def config_Path():
    result = modelSystem.runShell("ps -p "+str(get_pid())+" -o args")
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


def serverURL():
    parser_file = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)   
    parser_file.read(config_Path())    
    sup_url= parser_file.get("inet_http_server","port")
    if("localhost" in sup_url):
        return str(sup_url)       
    url=re.search("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$",sup_url) 
    return str(url.string)

server = ServerProxy("http://"+serverURL()+"/RPC2")

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
