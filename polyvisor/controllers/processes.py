import sys
import os
from polyvisor.finder import configPolyvisorPath
from polyvisor.models.modelPolyvisor import PolyVisor
# Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
from polyvisor.models.modelProcess import Process, clear_all_process_log, read_stdErr_logFile, read_stdOut_logFile, startAllProcesses, startProcessByName, startProcessGroup, stopAllProcesses, stopProcessByName, clear_process_log, stopProcessGroup, tail_stdErr_logFile, tail_stdOut_logFile, get_process_affinity_CPU,set_process_affinity_CPU

# get all processes info
def get_all_processes_model():
    return Process.getAllProcessInfo()

# #start all processes, return array result
# def start_all_processes_model():
#     return startAllProcesses()    

#start process by name, always return True unless error
# def start_process_by_name_model(name):
#     return startProcessByName(name)

#stop process by name, always return True unless error
# def stop_process_by_name_model(name):
#     return stopProcessByName(name)

#stop ALL process, return array result
def stop_all_processes_model():
    return stopAllProcesses()

# start group of process by group name, return array result
def start_process_group_model(group):
    return startProcessGroup(group)

# stop group of process by group name, return array result
def stop_process_group_model(group):
    return stopProcessGroup(group)
#get all data StdOut  of process by name
def read_stdOut_process_model(name, offset, length):
    return read_stdOut_logFile(name , offset, length)

#get all data StdErr  of process by name
def read_stdErr_process_model(name):
    return read_stdErr_logFile(name)

# clear stdOut, stdErr of process by name
def clear_log_process_by_name_model(name):
    return clear_process_log(name)

# tail stdOut log file of process with name
def tail_stdOut_logFile_model(name, offset, length):
    return tail_stdOut_logFile(name, offset, length)

# tail stdErr log file of process with name
def tail_stdErr_logFile_model(name, offset, length):
    return tail_stdErr_logFile(name, offset, length)

# clear process log with name
def clear_process_log_model(name):
    return clear_process_log(name)

# clear all process log
def clear_all_process_log_model():
    return clear_all_process_log()

# auto clear log of process after a limited amount of bytes
def auto_clear_log_process_model(name, limit):
    return True

# View current affinity list in CPU, Return can be range(0-5), single number, or many numbers(3,6,7) unless error
def process_Core_Index(pid):
    result = get_process_affinity_CPU(pid)
    if(result.find("failed")!=-1):
        return False
    return result

# Set affinity list in CPU, Return True unless error, parameter core_index SHOULD be STRING, value can be "3,4,9" or "4-12"
def set_Process_Core_Index(pid, core_index):
    return set_process_affinity_CPU(pid,core_index)


def stop_processes_by_name_model(*name):

    options = {
        "config_file": configPolyvisorPath()  # Replace with the actual file path
    }
    poly_visor = PolyVisor(options)
    poly_visor.refresh()
    result = poly_visor.stop_processes(*name)
    return result
    

def restart_processes_by_name_model(*name):

    options = {
        "config_file": configPolyvisorPath()  # Replace with the actual file path
    }
    poly_visor = PolyVisor(options)
    poly_visor.refresh()
    result = poly_visor.restart_processes(*name)
    return result    

def start_processes_by_name_model(*name):

    options = {
        "config_file": configPolyvisorPath()  # Replace with the actual file path
    }
    poly_visor = PolyVisor(options)
    poly_visor.refresh()
    result = poly_visor.start_processes(*name)
    return result


def stop_all_processes_model():

    options = {
        "config_file": configPolyvisorPath()  # Replace with the actual file path
    }
    poly_visor = PolyVisor(options)
    poly_visor.refresh()
    result = poly_visor.stop_all_processes()
    return result


def start_all_processes_model():

    options = {
        "config_file": configPolyvisorPath()  # Replace with the actual file path
    }
    poly_visor = PolyVisor(options)
    poly_visor.refresh()
    result = poly_visor.start_all_processes()
    return result
