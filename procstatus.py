import os
from machinestatus import server
import json


#Get Information of process by name
def process_Info(process_name):
    return server.supervisor.getProcessInfo(process_name)
    
#Get logfile ouput of process by name
def process_readLogFile_out(name,offset, length):
    return server.supervisor.readProcessStdoutLog(name,offset,length)
    
#Get logfile error of process bt name
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
