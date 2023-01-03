import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(1,parent)
from finder import runShell
class System:

    def __init__(self):
        pass 
    
    #Get stats of each core CPU
    @property
    def each_cpu_usage(self):  
        output = runShell("""grep 'cpu' /proc/stat | awk -v OFS="\t" 'NR==1{$11="usr"}NR>1{$11=($2*100)/($2+$3+$4+$5+$6+$7+$8+$9+$10)}2' | awk '{printf($1" %.2f\\n",$11)}'| tail -n +2""")
        result = output.replace("st","")               
        result = result.replace("us,", "")
        result = result.replace(":","")
        result = result.replace(",",".")
        result = result.replace("cpu","")
        result = dict(zip(result.split()[::2], result.split()[1::2]))
        #Convert dict value from string to float
        try:

            result_float = dict(zip(result.keys(), [float(value) for value in result.values()]))
            return result_float
        except:
            return result

    #Get overall %CPU stats
    @property
    def current_cpu_usage(self):
        output = runShell("""top -bn 1  | grep '^%Cpu' | tail -n 1 | awk '{print $2}'""")
        result = output.replace("\n", "")    
        result = result.replace(",",".")    
        return float(result)

    #Get %Memory stats
    @property
    def memory_status(self):
        output = runShell("""free | grep Mem | awk '{printf "%.2f",(($3/$2) * 100)}'""")
        result = output.replace("\n", "")
        result = result.replace(",",".")
        return float(result)
        
    #Get info about machine hardware
    @property
    def machine_spec(self):
        output = runShell("""cat /proc/cpuinfo | grep 'model name' | uniq && free -g -h -t | grep Mem | awk '{print "TotalMemory: " $2}'""")
        result = output.replace("model name", "CPU")
        result += "CPUs: "+str(os.cpu_count())
        result = result.replace("\t", "")
        result = result.replace(",",".")
        result = (dict([line.split(': ') for line in result.splitlines()]))
        result["CPUs"]=int(os.cpu_count())
        return result

    # #Get CPU Stats for Chart
    # @property
    # def cpu_list(self):
    #     return cpuList

    # #Get Mem Stats for Chart
    # @property
    # def memory_list(self):
    #     return memoryList