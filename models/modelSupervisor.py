from xmlrpc.client import ServerProxy
import re
import configparser 
import os
from collections import OrderedDict
from modelSystem import runShell

#To get multiple value in config file
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

server = ServerProxy("http://localhost:10019/RPC2")


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
    #Get serverurl Supervisor
    def serverURL(self):
        parser_file = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)   
        parser_file.read(self.configPath())
        sup_url= parser_file.get("inet_http_server","port")
        return str(sup_url)

    @property
    #Get config file path of Supervisord when it running on machine
    def configPath(self):
        result = runShell("ps -p "+self.pid+" -o args")
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
