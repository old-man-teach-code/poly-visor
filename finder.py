import os
import re
import configparser
from collections import OrderedDict
import threading
from time import sleep

isThen_Secs=True
cpuList=[]
memoryList=[]

#To get multiple value in config file
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

# Get pid supervisord by name in linux with shell
def get_pid():
    result = runShell("pgrep supervisord")
    result = result.replace("\n", "")
    return result


# Get config file path of Supervisord when it running on machine
def configPath():
    result = runShell("ps -p "+str(get_pid())+" -o args")
    path = ""
    s = re.findall(r'(\/.*?\.[\w:]+)', result)
    try:
        lis = s[1].split()
        for x in lis:
            if (r".conf" in x or r".ini" in x):
                path += x
    except:
        lis2 = s[0].split()
        for x in lis2:
            if (r".conf" in x or r".ini" in x):
                path += x

    if path == "" or not path:
        path = "Can't find config path of Supervisord"
    return path

# Get include process config files path
def get_proc_config_path():
    config = configparser.RawConfigParser(
        dict_type=MultiOrderedDict, strict=False)
    config.read(configPath())
    #path = config['include']['files']
    path = config.get("include", "files")

    return path

# Get serverurl Supervisor
def serverURL():
    parser_file = configparser.RawConfigParser(
        dict_type=MultiOrderedDict, strict=False)
    parser_file.read(configPath())
    sup_url = parser_file.get("inet_http_server", "port")
    # if("localhost" in sup_url):
    #     return str(sup_url)
    # else:
    #     url=re.search("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$",sup_url)
    #     return str(url)

    # if localhost is in serverurl, replace it with blank
    if ("localhost" in sup_url):
        sup_url = sup_url.replace("localhost", "")
    return sup_url

# Get path of process with pid when it running
def get_path_proc(proc_PID):
    return runShell("readlink -f /proc/"+str(proc_PID)+"/exe")


def path_sup_logfile():
    config = configparser.RawConfigParser(
        dict_type=MultiOrderedDict, strict=False)
    config.read(configPath())
    path = config.get("supervisord", "logfile")
    return path

# Run shell command and return output
def runShell(command):
    stream = os.popen(command)
    output = stream.read()
    return output

# Check supervisord is running as Root, return True, or False
def check_supervisor_isRunning_asRoot():
    output = runShell("ps -p "+get_pid()+" -o user | tail -n 1")
    result = output.replace("\n", "")
    if result == "root":
        return True
    return False

#Get list CPU stats and Memory by number of "sec" seconds
def get_list_stats_cpu_mem(sec):
    #modify isThen_Secs and cpuList variable
    global isThen_Secs
    global cpuList
    while True:
        if isThen_Secs==True:
            #get cpu stats
            Cpu_output = runShell("""top -bn 1  | grep '^%Cpu' | tail -n 1 | awk '{print $2"%"}'""")
            result = Cpu_output.replace("\n", "")
            result = result.replace("%","")
            if len(cpuList)>=10:
                cpuList.pop(0)
            cpuList.append(result)
            #get memory stats
            Mem_output= runShell("""free -g -h -t | grep Mem | awk '{printf "%.2f\\n",(($3/$2) * 100)}'""")
            if len(memoryList)>=10:
                memoryList.pop(0)
            Mem_output = Mem_output.replace("\n","")
            memoryList.append(Mem_output)
            isThen_Secs=False
            sleep(sec)
        elif isThen_Secs==False:
            isThen_Secs=True

#Run func get_list_stats_cpu_mem with thread
def start_getList_stats(seconds):
    thr1 = threading.Thread(target=get_list_stats_cpu_mem,args=(seconds,))
    thr1.start()
start_getList_stats(3)