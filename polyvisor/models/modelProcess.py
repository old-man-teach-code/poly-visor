import subprocess
import sys
import os
# Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
from polyvisor.models.modelSupervisor import server
from polyvisor.finder import runShell


class Process:
    name = ""
    group = ""
    description = ""
    start = ""
    stop = ""
    state = ""
    statename = ""
    spawnerr = ""
    exitstatus = ""
    logfile = ""
    stdout_logfile = ""
    stderr_logfile = ""
    pid = 0
    core_index = ""

    def __init__(self, name, group,  start, stop, state, statename, spawnerr, exitstatus, logfile, stdout_logfile, stderr_logfile, pid, description):
        self.name = name
        self.group = group
        self.start = start
        self.stop = stop
        self.state = state
        self.statename = statename
        self.spawnerr = spawnerr
        self.exitstatus = exitstatus
        self.logfile = logfile
        self.stdout_logfile = stdout_logfile
        self.stderr_logfile = stderr_logfile
        self.pid = pid
        self.description = description
        if self.pid :
            self.core_index = get_process_affinity_CPU(self.pid)
        else:
            self.core_index = None    
        

    @classmethod
    def getAllProcessInfo(self):
        

        # get all process info from supervisor and return a list of Process objects
        processInfo = server.supervisor.getAllProcessInfo()
        # append get process afinity CPU to processInfo
        
        processList = []
        for process in processInfo:
            processList.append(Process(
                process['name'],
                process['group'],
                process['start'],
                process['stop'],
                process['state'],
                process['statename'],
                process['spawnerr'],
                process['exitstatus'],
                process['logfile'],
                process['stdout_logfile'],
                process['stderr_logfile'],
                process['pid'],
                process['description'],
                ))
            
                
        return processList

# start all processes, return array result
def startAllProcesses():
    return server.supervisor.startAllProcesses()

# start process by name, always return True unless error
def startProcessByName(name):
    return server.supervisor.startProcess(name)

# stop process by name, always return True unless error
def stopProcessByName(name):
    return server.supervisor.stopProcess(name)

# stop all process, return array result
def stopAllProcesses():
    return server.supervisor.stopAllProcesses()


# start group of process by group name, return array result
def startProcessGroup(group):
    return server.supervisor.startProcessGroup(group)

# stop group of process by group name, return array result
def stopProcessGroup(group):
    return server.supervisor.stopProcessGroup(group)

#return all data from stdOut in logfile of process with name
def read_stdOut_logFile(name, offset, length):
    return server.supervisor.readProcessStdoutLog(name, offset, length)

#return all data from stdErr in logfile of process with name
def read_stdErr_logFile(name):
    return server.supervisor.readProcessStderrLog(name,0,0)

#clear process stdOut,stdErr log by name, always return True unless error
def clear_process_log(name):
    return server.supervisor.clearProcessLogs(name)

# tail stdOut log file of process with name
def tail_stdOut_logFile(name, offset, length):
    return server.supervisor.tailProcessStdoutLog(name, offset, length)

# tail stdErr log file of process with name
def tail_stdErr_logFile(name, offset, length):
    return server.supervisor.tailProcessStderrLog(name, offset, length)

# clear process log  with name
def clear_process_log(name):
    return server.supervisor.clearProcessLogs(name)

# clear all process log
def clear_all_process_log():
    return server.supervisor.clearAllProcessLogs()

# View current affinity list in CPU, Return canbe range(0-5), single number, or many numbers(3,6,7) Return FALSE if error
def get_process_affinity_CPU(pid):
    if str(pid).isnumeric()==False:
        return False
    else:
        output = runShell("taskset -cp "+str(pid))
        if("failed" in output):
            return False
        
        char_index= output.find(":")
        output=output[char_index+2::].replace('\n','')
        # Split the output by comma first
        parts = output.split(',')

        # Initialize an empty list to store the final result
        result = []

        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                result.extend(range(start, end + 1))
            else:
                result.append(int(part))

        return result
        

def set_process_affinity_CPU(pid, core_index):
    try:
        terminal_command = [
        "pkexec",
        "bash",
        "-c",
        "taskset -cp " + str(core_index) + " " + str(pid) 
        ]
        # run the terminal_command if success return True, else return False
        subprocess.check_output(terminal_command)
        return True
    except subprocess.CalledProcessError:
        return False
        

    
    

