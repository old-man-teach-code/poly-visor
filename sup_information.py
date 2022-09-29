from unicodedata import name
from xmlrpc.client import ServerProxy
import json
import os

server = ServerProxy('http://192.168.32.130:60000/RPC2')


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
def process_memory_usage(pid_process):
    stream = os.popen("ps -o pid,psr,%cpu,%mem,comm -p "+ str(pid_process))
    output = stream.read()
    return output
    
#Get Host Name
def get_hostname():
    stream = os.popen("hostname")
    output = stream.read()
    return output
        

# def get_process_logstdout(name):
#     process_Information=process_Info(name)
#     jsonRaw = json.dumps(process_Information)
#     jsonParse = json.loads(jsonRaw)
#     path_logfile= jsonParse["stdout_logfile"]

print(get_hostname())

#print("grep --color VmSwap /proc/"+ str(3) +"/status")
#print(process_swap(process_PID("Demo_1")))

