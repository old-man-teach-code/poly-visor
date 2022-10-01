from ctypes.wintypes import PLARGE_INTEGER
from time import sleep, thread_time
from xmlrpc.client import ServerProxy
import os

from urllib3 import Retry
from finder import get_sup_serverurl, get_sup_config_path

#server = ServerProxy('http://localhost:10019/RPC2')

#Server can be auto set by read logfile
server = ServerProxy(str(get_sup_serverurl())+"/RPC2")


#Get Supervior State 
def sup_State() :
    return server.supervisor.getState()

#Get Supervisor PID
def sup_PID():
    return server.supervisor.getPID()

#Get Supervisor Log ()
def sup_readAllLog():
    print(server.supervisor.readLog(0,0))

#Get Supervisor API Version
def sup_APIVer():
    return server.supervisor.getAPIVersion()

#Get Superivsor Version
def sup_Version():
    return server.supervisor.getSupervisorVersion()

#Get Supervisor Indentification
def sup_Indentification():
    return server.supervisor.getIdentification()

#Get Information of all process in machine
def process_AllInfo():
    return server.supervisor.getAllProcessInfo()

#Get Host Name
def get_hostname():
    stream = os.popen("hostname")
    output = stream.read()
    return output

#Get current each core CPU Usage
def get_each_cpu_usage():
    stream = os.popen("""top 1 -bn1  | grep '^%Cpu' |awk '{print $1,$2,$3"\\n"$18,$19,$20,$21}'""")
    output = stream.read()    
    b = output.replace("st ","")               #Output cpu stats
    result=b.replace(" us,","")
    return  result

#Get mem, cpu, core of process running on
def process_memory_usage(pid_porcess):
    stream = os.popen("ps -o pid,psr,%cpu,%mem,comm -p "+ str(pid_porcess))
    output = stream.read()
    return output

#Get current CPU Usage
def get_current_cpu_usage():
    stream = os.popen("""top -bn 1  | grep '^%Cpu' | tail -n 1 | awk '{print $2"%"}'""")
    output = stream.read()
    return  output

#Get Memory status
def get_memory_status():
    stream = os.popen("""free -g -h -t | grep Mem | awk '{print ($3/$2) * 100"%"}'""")
    output = stream.read()
    return  output

#Get total memory, CPU model, processor spec GB
def get_machine_spec():
    stream = os.popen("""cat /proc/cpuinfo | grep 'model name' | uniq && free -g -h -t | grep Mem | awk '{print "Total Memory: " $2}'""")
    output = stream.read()
    output+= "CPUs: "+str(os.cpu_count())
    return  output.replace("model name","CPU Model Name")

#Get data from config file of supervisord
def get_data_sup_config_file(path_file):
    fil = open(path_file,"r")
    data = fil.read()
    fil.close()
    return data


