import sys
import os
#Get PARENT path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
#insert into PYTHONPATH
sys.path.insert(1,parent)
from models.modelSupervisor import Supervisor

# get Supervisor object from modelSupervisor
def get_supervisor():
    a = Supervisor()
    return a


def restart_supervisor_model():
    a = Supervisor()
    return a.restart

# clear log
def clear_log_model():
    a = Supervisor()
    return a.clear_log