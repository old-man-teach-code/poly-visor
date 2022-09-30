from unicodedata import name
from xmlrpc.client import ServerProxy
import json
import os
import configparser
from os.path import exists
from pathlib import Path

server = ServerProxy('http://localhost:10019/RPC2')


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

#Get Information of process by name
def process_Info(process_name):
    return server.supervisor.getProcessInfo(process_name)
    
#Get Information of all process
def process_AllInfo():
    return server.supervisor.getAllProcessInfo()

#Get logfile ouput of process
def process_readLogFile_out(name,offset, length):
    return server.supervisor.readProcessStdoutLog(name,offset,length)
    
#Get logfile error of process
def process_readLogFile_err(name, offset, length):
    return server.supervisor.readProcessStderrLog(name, offset,length)

#Get process PID
def process_PID(name):
    process_Information=process_Info(name)
    jsonRaw = json.dumps(process_Information)
    jsonParse = json.loads(jsonRaw)
    return jsonParse["pid"]

#Get swap used by process
def process_swap(pid_process):
    stream = os.popen("grep --color VmSwap /proc/"+ str(pid_process)+"/status")
    output = stream.read()
    return output

#Get mem, cpu, core of process running on
def process_memory_usage(pid_porcess):
    stream = os.popen("ps -o pid,psr,%cpu,%mem,comm -p "+ str(pid_porcess))
    output = stream.read()
    return output
    
#Get Host Name
def get_hostname():
    stream = os.popen("hostname")
    output = stream.read()
    return output
        
#Get current CPU Usage
def get_current_cpu_usage():
    stream = os.popen("""top -bn 1  | grep '^%Cpu' | tail -n 1 | awk '{print $2"%"}'""")
    output = stream.read()
    return  output

#Get current each core CPU Usage
def get_each_cpu_usage():
    stream = os.popen("""top 1 -bn1  | grep '^%Cpu' |awk '{print $1,$2,$3"\\n"$18,$19,$20,$21}'""")
    output = stream.read()
    return  output
    # a = get_each_cpu_usage()
    # b = a.replace("st ","")               Output cpu stats
    # c=b.replace(" us,","")
    # print(c)

#Get Memory status
def get_memory_status():
    stream = os.popen("free | grep Mem | awk '{print ($3/$2) * 100.0}'")
    output = stream.read()
    return  output

#Get path of supervisord config file
def sup_config_path():
    stream = os.popen("ps aux | grep supervisord")
    output = stream.read()
    lis= output.split()
   
    for x in lis:
        path=Path(x)
        if path.is_file()==False:
                lis.remove(x)

            

   
    return lis


print(get_memory_status())

