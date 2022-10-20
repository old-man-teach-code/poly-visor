import sys
import os
# Get PARENT path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
# get Supervisor object from modelSupervisor
from models.modelSupervisor import Supervisor

def get_supervisor():
    a = Supervisor()
    return a

# restart supervisor
def restart_supervisor_model():
    a = Supervisor()
    return a.restart

# shut down supervisor
def shutdown_supervisor_model():
    a = Supervisor()
    return a.shutdown

# clear log
def clear_log_model():
    a = Supervisor()
    return a.clear_log

# reload config supervisor, return array result [[added, changed, removed]]
def reload_config_model():
    a = Supervisor()
    return a.reloadConfig()