import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(1,parent)
from finder import runShell
class System:

    def __init__(self):
        pass 

    @property
    def each_cpu_usage(self): #Get stats of each core CPU 
        stream = os.popen(
            """top 1 -bn1  | grep '^%Cpu' |awk '{print $1,$2,$3"\\n"$18,$19,$20,$21}'""")
        output = stream.read()
        b = output.replace("st ","")               
        result=b.replace(" us,","")
        result = result.replace("\n", " ")
        result = result.replace("us,", "")
        result = result.replace(":", " ")
        result = dict(zip(result.split()[::2], result.split()[1::2]))
        return result     
    @property
    def current_cpu_usage(self):
        stream = os.popen("""top -bn 1  | grep '^%Cpu' | tail -n 1 | awk '{print $2"%"}'""")
        output = stream.read()  
        output = output.replace("\n", "")        
        return output
    @property
    def memory_status(self):
        stream = os.popen(
            """free -g -h -t | grep Mem | awk '{print ($3/$2) * 100"%"}'""")
        output = stream.read()
        output = output.replace("\n", "")
        return output

    @property
    def machine_spec(self):
        result = runShell("""cat /proc/cpuinfo | grep 'model name' | uniq && free -g -h -t | grep Mem | awk '{print "TotalMemory: " $2}'""")
        result = result.replace("model name", "CPU")
        result += "CPUs: "+str(os.cpu_count())
        result = result.replace("\t", "")
        result = (dict([line.split(': ') for line in result.splitlines()]))
        return result
