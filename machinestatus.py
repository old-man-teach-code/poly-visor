from xmlrpc.client import ServerProxy
import os

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
    stream = os.popen("free | grep Mem | awk '{print ($3/$2) * 100.0}'")
    output = stream.read()
    return  output