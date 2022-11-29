import sys
import os
import configparser



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

# get all log of supervisor since it run
def all_log_supervisord():
    a = Supervisor()
    return a.all_log
    
#Clear all log of process when it running, return array result status info
def clear_all_log_of_processes():
    a= Supervisor()
    return a.clear_all_log_processes

def createConfig(process_name, command):
    config = configparser.ConfigParser()
    config['program:' + process_name] = {
        'command': command,
        'autostart': 'true',
        'autorestart': 'true',
        'stdout_logfile': '/var/log/' + process_name +'.out.log',
        'stderr_logfile': '/var/log/' + process_name +'.err.log',
    }
    with open('/etc/supervisor/conf.d/' + process_name + '.ini', 'w') as configfile:
        config.write(configfile)


# create updateConfig function to update the config file based on the key
def updateConfig(process_name, key, value):
    config = configparser.ConfigParser()
    config.read('/etc/supervisor/conf.d/test.ini')
    config['program:' + process_name][key] = value
    with open('/etc/supervisor/conf.d/' + process_name + '.ini', 'w') as configfile:
        config.write(configfile)



# create updateConfig function to update the config file based on the key
def updateConfig(process_name, key, value):
    config = configparser.ConfigParser()
    config.read('/etc/supervisor/conf.d/test.ini')
    config['program:' + process_name][key] = value
    with open('/etc/supervisor/conf.d/' + process_name + '.ini', 'w') as configfile:
        config.write(configfile)    