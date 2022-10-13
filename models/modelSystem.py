import os


class System:
    each_cpu_usage = {}
    current_cpu_usage = 0
    memory_status = 0
    machine_spec = {}
    host_name = ""

    def __init__(self, each_cpu_usage, current_cpu_usage, memory_status, machine_spec, host_name):
        self.each_cpu_usage = each_cpu_usage
        self.current_cpu_usage = current_cpu_usage
        self.memory_status = memory_status
        self.machine_spec = machine_spec
        self.host_name = host_name
    








    def get_each_cpu_usage():
        stream = os.popen(
            """top 1 -bn1  | grep '^%Cpu' |awk '{print $1,$2,$3"\\n"$18,$19,$20,$21}'""")
        output = stream.read()
        b = output.replace("st ", "")
        result = b.replace(" us,", "")
        return result

    def get_current_cpu_usage():
        stream = os.popen(
            """top -bn 1  | grep '^%Cpu' | tail -n 1 | awk '{print $2"%"}'""")
        output = stream.read()
        return output

    def get_memory_status():
        stream = os.popen(
            """free -g -h -t | grep Mem | awk '{print ($3/$2) * 100"%"}'""")
        output = stream.read()
        return output

    def get_machine_spec():
        stream = os.popen(
            """cat /proc/cpuinfo | grep 'model name' | uniq && free -g -h -t | grep Mem | awk '{print "TotalMemory: " $2}'""")
        output = stream.read()
        output += "CPUs: "+str(os.cpu_count())
        return output.replace("model name", "CPUModelName")
