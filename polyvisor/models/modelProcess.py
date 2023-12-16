import subprocess
import sys
import os
import weakref
import logging
import psutil
from xmlrpc.client import ServerProxy
from polyvisor.controllers.utils import parse_dict, send_webhook_alert
# Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
from polyvisor.models.modelSupervisor import error, info, send, server, warning
from polyvisor.finder import runShell

log = logging.getLogger("polyvisor")

# class Process:
#     name = ""
#     group = ""
#     description = ""
#     start = ""
#     stop = ""
#     state = ""
#     statename = ""
#     spawnerr = ""
#     exitstatus = ""
#     logfile = ""
#     stdout_logfile = ""
#     stderr_logfile = ""
#     pid = 0
#     core_index = ""

#     def __init__(self, name, group,  start, stop, state, statename, spawnerr, exitstatus, logfile, stdout_logfile, stderr_logfile, pid, description):
#         self.name = name
#         self.group = group
#         self.start = start
#         self.stop = stop
#         self.state = state
#         self.statename = statename
#         self.spawnerr = spawnerr
#         self.exitstatus = exitstatus
#         self.logfile = logfile
#         self.stdout_logfile = stdout_logfile
#         self.stderr_logfile = stderr_logfile
#         self.pid = pid
#         self.description = description
#         if self.pid :
#             self.core_index = get_process_affinity_CPU(self.pid)
#         else:
#             self.core_index = None    
        

#     @classmethod
#     def getAllProcessInfo(self):
        

#         # get all process info from supervisor and return a list of Process objects
#         processInfo = server.supervisor.getAllProcessInfo()
#         # append get process afinity CPU to processInfo
        
#         processList = []
#         for process in processInfo:
#             processList.append(Process(
#                 process['name'],
#                 process['group'],
#                 process['start'],
#                 process['stop'],
#                 process['state'],
#                 process['statename'],
#                 process['spawnerr'],
#                 process['exitstatus'],
#                 process['logfile'],
#                 process['stdout_logfile'],
#                 process['stderr_logfile'],
#                 process['pid'],
#                 process['description'],
#                 ))
            
                
#         return processList
# Enumeration class defining various process states.
class ProcessStates:
    STOPPED = 0
    STARTING = 10
    RUNNING = 20
    BACKOFF = 30
    STOPPING = 40
    EXITED = 100
    FATAL = 200
    UNKNOWN = 1000

# Tuple of states representing processes that are stopped.
STOPPED_STATES = (
    ProcessStates.STOPPED,
    ProcessStates.EXITED,
    ProcessStates.FATAL,
    ProcessStates.UNKNOWN
)

# Tuple of states representing processes that are running or starting.
RUNNING_STATES = (
    ProcessStates.RUNNING,
    ProcessStates.BACKOFF,
    ProcessStates.STARTING
)

# Tuple of states representing processes that are signallable (can be started, stopped, etc.).
SIGNALLABLE_STATES = (
    ProcessStates.RUNNING,
    ProcessStates.STARTING,
    ProcessStates.STOPPING
)

# Class representing a process, inheriting from the built-in dict class.
class Process(dict):

    # Null values for a process.
    Null = {"running": False, "pid": None, "state": None, "statename": "UNKNOWN"}

    # Constructor for the Process class.
    def __init__(self, supervisor, *args, **kwargs):
        # Initialize with default values
        super(Process, self).__init__(self.Null)

        # Update with arguments and keyword arguments
        if args:
            self.update(args[0])
        self.update(kwargs)

        supervisor_name = supervisor["name"]
        full_name = f"{self.get('group', '')}:{self.get('name', '')}"
        uid = f"{supervisor_name}:{full_name}"

        self.log = log.getChild(uid)
        self.supervisor = weakref.proxy(supervisor)

        self["full_name"] = full_name
        self["running"] = self["state"] in RUNNING_STATES
        self["supervisor"] = supervisor_name
        self["host"] = supervisor["host"]
        self["uid"] = uid

        # Calculate core_index if pid is available
        self["core_index"] = get_process_affinity_CPU(self["pid"]) if self["pid"] else None

        self["network_io_counters"] = self.get_network_io_counters()
        self["network_connections"] = self.get_network_connections()
        self["network_interface_addrs"] = self.get_network_interface_addrs()
        self["network_interface_stats"] = self.get_network_interface_stats()

    # Property to access the supervisor's server.
    @property
    def server(self):
        return self.supervisor.server.supervisor

    # Property to get the full name of the process.
    @property
    def full_name(self):
        return self["full_name"]

    # Method to handle supervisor events related to the process.
    # def handle_event(self, event):
    #     event_name = event["eventname"]
    #     if event_name.startswith("PROCESS_STATE"):
    #         payload = event["payload"]
    #         proc_info = payload.get("process")
    #         if proc_info is not None:
    #             proc_info = parse_dict(proc_info)
    #             old = self.update_info(proc_info)
    #             if old != self:
    #                 old_state, new_state = old["statename"], self["statename"]
    #                 send(self, event="process_changed")
    #                 if old_state != new_state:
    #                     info(
    #                         "{} changed from {} to {}".format(
    #                             self, old_state, new_state
    #                         )
    #                     )

    # Method to read information about the process from the supervisor.
    def read_info(self):
        proc_info = dict(self.Null)
        try:
            from_serv = parse_dict(self.server.getProcessInfo(self.full_name))
            proc_info.update(from_serv)
        except Exception as err:
            self.log.warn("Failed to read info from %s: %s", self["uid"], err)
        return proc_info

    # Method to update process information based on the provided info.
    def update_info(self, proc_info):
        old = dict(self)
        proc_info["running"] = proc_info["state"] in RUNNING_STATES
        self.update(proc_info)
        return old

    # Method to refresh process information by reading from the supervisor.
    def refresh(self):
        proc_info = self.read_info()
        proc_info = parse_dict(proc_info)
        self.update_info(proc_info)

    # Method to start the process.
    def start(self):
        try:
            send_webhook_alert(self.supervisor.webhook_url, "Start process {}".format(self["uid"]))
            result = self.server.startProcess(self.full_name)
            if result:
                info("Start process {} successfully".format(self["uid"]))
                return "The process {} has been started".format(self["uid"])
            else:
                info("Failed to start process {}".format(self["uid"]))
                return "Failed to start {}".format(self["uid"])

        except:
            message = "Error trying to start {}!".format(self)
            error(message)
            self.log.exception(message)

    # Method to stop the process.
    def stop(self):
        try:
            send_webhook_alert(self.supervisor.webhook_url, "Stop process {}".format(self["uid"]))
            result = self.server.stopProcess(self.full_name)
            if result:
                info("Stop process {} successfully".format(self["uid"]))
                return "The process {} has been stopped".format(self["uid"])
            else:
                info("Failed to stop process {}".format(self["uid"]))
                return "Failed to stop {}".format(self["uid"])

        except:
            message = "Failed to stop {}".format(self["uid"])
            warning(message)
            self.log.exception(message)

    # Method to restart the process.
    def restart(self):
        if self["running"]:
            self.stop()
        self.start()
        info("Restart process {}".format(self["uid"]))
        send_webhook_alert(self.supervisor.webhook_url, "Restart process {}".format(self["uid"]))

    # Method to stop all processes.
    def stopAll(self):
        try:
            send_webhook_alert(self.supervisor.webhook_url, "Stop all processes")
            self.server.stopAllProcesses()
            info("Stop all processes successfully")
        except:
            message = "Failed to stop all processes!"
            warning(message)
            self.log.exception(message)

    # Method to start all processes.
    def startAll(self):
        try:
            send_webhook_alert(self.supervisor.webhook_url, "Start all processes")
            self.server.startAllProcesses()
            info("Start all processes successfully")
        except:
            message = "Failed to start all processes!"
            warning(message)
            self.log.exception(message)

    # Method to get network I/O counters for the process.
    def get_network_io_counters(self):
        try:
            process = psutil.Process(self["pid"])
            network_counters = process.io_counters()
            if network_counters is None:
                # return an array with 6 elements of 0
                return [0, 0, 0, 0, 0, 0]
            else:
                return network_counters
        except psutil.NoSuchProcess:
            return [0, 0, 0, 0, 0, 0]

    # Method to get network connections associated with the process.
    def get_network_connections(self):
        try:
            process = psutil.Process(self["pid"])
            connections = process.connections(kind='inet')  # Filter by IPv4 connections
            return connections
        except psutil.NoSuchProcess:
            return []

    # Method to get network interface addresses.
    def get_network_interface_addrs(self):
        try:
            interface_addrs = psutil.net_if_addrs()
            return interface_addrs
        except Exception as e:
            return {}

    # Method to get network interface statistics.
    def get_network_interface_stats(self):
        try:
            interface_stats = psutil.net_if_stats()
            return interface_stats
        except Exception as e:
            return {}

    # String representation of the process.
    def __str__(self):
        return "{0} on {1}".format(self["name"], self["supervisor"])

    # Equality comparison for processes.
    def equal(self, proc):
        p1, p2 = dict(self), dict(proc)
        p1.pop("description")
        p1.pop("now")
        p2.pop("description")
        p2.pop("now")
        return p1 == p2

    # Inequality comparison for processes.
    def notEqual(self, proc):
        return not self == proc

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
        if("failed to"in output):
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
            # if the part is only [''] return empty list
            elif part == '':
                return False 
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
        

    
    

