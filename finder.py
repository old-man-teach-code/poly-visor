import os
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
   

#Get config file path of Supervisord when it running on machine
def configPath():
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

#Get include process config files path
def get_proc_config_path():
    config = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)   
    config.read(configPath())
    #path = config['include']['files']   
    path = config.get("include","files")
    
    return path

#Get serverurl Supervisor
def serverURL():
    parser_file = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)   
    parser_file.read(configPath())    
    sup_url= parser_file.get("inet_http_server","port")
    # if("localhost" in sup_url):
    #     return str(sup_url)       
    # else:
    #     url=re.search("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$",sup_url) 
    #     return str(url)

    
    #if localhost is in serverurl, replace it with blank
    if("localhost" in sup_url):
        sup_url=sup_url.replace("localhost","")
    return sup_url

#Get path of process with pid when it running
def get_path_proc(proc_PID):
    return  runShell("readlink -f /proc/"+str(proc_PID)+"/exe")

#Get path of logfile supervisord
def path_sup_logfile():
    config = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)   
    config.read(configPath())
    path = config.get("supervisord","logfile")
    return path
#Run shell command and return output
def runShell(command):
    stream = os.popen(command)
    output = stream.read()
    return output