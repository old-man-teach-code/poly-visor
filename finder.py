from collections import OrderedDict
import os
import re
import configparser

#To get multiple value in config file
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

#Get config file path of Supervisord when it running on machine
def get_sup_config_path():
    output=""
    stream = os.popen("""ps ux | awk '/.conf/ && /supervisord/ || /.ini/ && /supervisord/' | head -n -2""")
    raw = stream.read()
    if("supervisord" not in raw):
         stream = os.popen("""sudo ps ux | awk '/.conf/ && /supervisord/ || /.ini/ && /supervisord/' | head -n -2""")
         output = stream.read()
    else:       
        output = raw
    path=""
    s = re.findall(r'(\/.*?\.[\w:]+)', output)
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
    config.read(get_sup_config_path())
    #path = config['include']['files']   
    path = config.get("include","files")
    
    return path

#Get serverurl Supervisor
def get_sup_serverurl():
    parser_file = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)   
    parser_file.read(get_sup_config_path())
    sup_url= parser_file.get("inet_http_server","port")
    return str(sup_url)

#Get path of process with pid when it running
def get_path_proc(proc_PID):
    from procstatus import process_PID
    stream = os.popen("readlink -f /proc/"+str(proc_PID)+"/exe")
    output = stream.read()
    return  output

#Get path of logfile supervisord
def get_path_sup_logfile():
    config = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)   
    config.read(get_sup_config_path())
    path = config.get("supervisord","logfile")
    return path