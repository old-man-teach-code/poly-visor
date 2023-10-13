import os
import concurrent.futures
import signal
import time
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.insert(1,parent)
from polyvisor.finder import runShell
class System:

    def __init__(self):
        pass 
    
    #Get stats of each core CPU
    # @property
    # def each_cpu_usage(self):  
    #     output = runShell("""grep 'cpu' /proc/stat | awk -v OFS="\t" 'NR==1{$11="usr"}NR>1{$11=($2*100)/($2+$3+$4+$5+$6+$7+$8+$9+$10)}2' | awk '{printf($1" %.2f\\n",$11)}'| tail -n +2""")
    #     result = output.replace("st","")               
    #     result = result.replace("us,", "")
    #     result = result.replace(":","")
    #     result = result.replace(",",".")
    #     result = dict(zip(result.split()[::2], result.split()[1::2]))
    #     #Convert dict value from string to float
    #     try:

    #         result_float = dict(zip(result.keys(), [float(value) for value in result.values()]))
    #         return result_float
    #     except:
    #         return result

    #Get stats of cores cpu
    @property
    def each_cpu_usage(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(cpu_Stats,1)
            valueList = future.result()
            return valueList

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
    

    property
    def cpu_usage_within_quota(self):
        current_usage = self.current_cpu_usage
        return current_usage <= self.cpu_quota

    @property
    def memory_usage_within_quota(self):
        current_memory = self.memory_status
        return current_memory <= self.memory_quota
    
    @property
    def monitor_resources(self):
        while True:
            if not self.cpu_usage_within_quota:
                # CPU usage exceeds the quota, take action (e.g., terminate a process)
                self.take_action_on_cpu_exceed()
            if not self.memory_usage_within_quota:
                # Memory usage exceeds the quota, take action (e.g., terminate a process)
                self.take_action_on_memory_exceed()
            time.sleep(self.monitor_interval)
    @property
    def take_action_on_cpu_exceed(self):
        # Implement your custom action here
        # For example, terminate a process consuming excessive CPU
        self.terminate_process_with_high_cpu()
    @property
    def take_action_on_memory_exceed(self):
        # Implement your custom action here
        # For example, terminate a process consuming excessive memory
        self.terminate_process_with_high_memory()

    @property
    def terminate_process_with_high_cpu(self):
        # Find the process consuming the most CPU and terminate it
        process_info = self.find_process_with_high_cpu()
        if process_info:
            pid, cpu_percent, command = process_info
            print(f"Terminating process {pid} consuming {cpu_percent}% CPU: {command}")
            os.kill(pid, signal.SIGKILL)


    @property
    def terminate_process_with_high_memory(self):
        # Find the process consuming the most memory and terminate it
        process_info = self.find_process_with_high_memory()
        if process_info:
            pid, mem_percent, command = process_info
            print(f"Terminating process {pid} consuming {mem_percent}% memory: {command}")
            os.kill(pid, signal.SIGKILL)


    @property
    def find_process_with_high_cpu(self):
        output = runShell("ps -eo pid,%cpu,command --sort=-%cpu | awk 'NR==2{print $1,$2,$3}'")
        if output:
            pid, cpu_percent, command = output.split()
            return int(pid), float(cpu_percent), command
        return None
    
    @property
    def find_process_with_high_memory(self):
        output = runShell("ps -eo pid,%mem,command --sort=-%mem | awk 'NR==2{print $1,$2,$3}'")
        if output:
            pid, mem_percent, command = output.split()
            return int(pid), float(mem_percent), command
        return None
def stats():
    cpuList={}
    file=open('/proc/stat','r') 
    Lines=file.readlines()
    for li in Lines:
        if "cpu" in li:
            line=li.split()
            total=int(line[1])+int(line[2])+int(line[3])+int(line[4])+int(line[5])+int(line[6])+int(line[7])+int(line[8])
            idle=int(line[4])+int(line[5])
            usage=total-idle
            cpuList[line[0]]=[total,idle,usage]
    #cpuList.pop(0)
    return cpuList

def cpu_Stats(time_Sec):
    if not str(time_Sec).isnumeric() or time_Sec<0.01:
        time_Sec=1;
    cpu_List=[]
    prev_CPU_List= stats()
    time.sleep(time_Sec)
    now_CPU_List=stats()
    #print(now_CPU_List)
    #print(now_CPU_List['cpu'][1])
    for x in prev_CPU_List:
        #print(prev_CPU_List[x][0])
        deltaTotal = now_CPU_List[x][0]-prev_CPU_List[x][0]
        deltaUsage= now_CPU_List[x][2]-prev_CPU_List[x][2]
        per = (deltaUsage/deltaTotal)*100
        cpuValue=round(per,2)
        cpu_List.append(cpuValue)
    return cpu_List[1:]

    # #Get CPU Stats for Chart
    # @property
    # def cpu_list(self):
    #     return cpuList

    # #Get Mem Stats for Chart
    # @property
    # def memory_list(self):
    #     return memoryList
