# from models.modelSupervisor import Supervisor
import sys
import os
import configparser
from flask import send_file
from polyvisor.models.modelSupervisor import Supervisor
from polyvisor.finder import configPolyvisorPath, split_config_path
from polyvisor.models.modelPolyvisor import PolyVisor

# Get PARENT path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
# get Supervisor object from modelSupervisor


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


def reload_config():
    a = Supervisor()
    return a.reload_config_model

# get all log of supervisor since it run


def all_log_supervisord():
    a = Supervisor()
    return a.all_log

# Clear all log of process when it running, return array result status info


def clear_all_log_of_processes():
    a = Supervisor()
    return a.clear_all_log_processes

# update the config file for a running process


def update_config(process_name):
    a = Supervisor()
    return a.update_config_model(process_name)

# reread and update by supervisorctl command

def get_config_info():
    a = Supervisor()
    return a.get_config_info_model

def reread_and_update():
    commandReread = 'supervisorctl reread'
    commandUpdate = 'supervisorctl update'
    os.system(commandReread)
    os.system(commandUpdate)

    
# Create config file for supervisor and check if file exist
def createConfig(
        pid,
        process_full_name, 
        command, 
        process_name='%(program_name)s_%(process_num)02d',
        numprocs=1, 
        umask='022', 
        numprocs_start=0, 
        priority=999, 
        autostart='true', 
        autorestart='true', 
        startsecs=1, 
        startretries=3, 
        exitcodes=0, 
        stopsignal='TERM', 
        stopwaitsecs=10, 
        stopasgroup='false', 
        killasgroup='false', 
        redirect_stderr='false', 
        stdout_logfile='AUTO',
        stderr_logfile='AUTO',
        stdout_logfile_maxbytes='50MB', 
        stdout_logfile_backups=10, 
        stdout_capture_maxbytes=0, 
        stdout_events_enabled=0, 
        stdout_syslog='false', 
        stderr_logfile_maxbytes='50MB', 
        stderr_logfile_backups=10, 
        stderr_capture_maxbytes=0, 
        stderr_events_enabled='false', 
        stderr_syslog='false', 
        environment='', 
        serverurl='AUTO', 
        directory='/tmp'):
    # if (os.path.isfile(split_config_path() + process_full_name + '.ini')):
    #     return False
    # else:
        config = configparser.ConfigParser(interpolation= None)
        process_full_name = process_full_name.split('_')[0]
        config['program:' + process_full_name] = {
            'command': command,
            'process_name': process_name,
            'numprocs': numprocs,
            'umask': umask,
            'numprocs_start': numprocs_start,
            'priority': priority,
            'autostart': autostart,
            'autorestart': autorestart,
            'startsecs': startsecs,
            'startretries': startretries,
            'exitcodes': exitcodes,
            'stopsignal': stopsignal,
            'stopwaitsecs': stopwaitsecs,
            'stopasgroup': stopasgroup,
            'killasgroup': killasgroup,
            'redirect_stderr': redirect_stderr,
            'stdout_logfile_maxbytes': stdout_logfile_maxbytes,
            'stdout_logfile': stdout_logfile,
            'stdout_logfile_backups': stdout_logfile_backups,
            'stdout_capture_maxbytes': stdout_capture_maxbytes,
            'stdout_events_enabled': stdout_events_enabled,
            'stdout_syslog': stdout_syslog,
            'stderr_logfile': stderr_logfile,
            'stderr_logfile_maxbytes': stderr_logfile_maxbytes,
            'stderr_logfile_backups': stderr_logfile_backups,
            'stderr_capture_maxbytes': stderr_capture_maxbytes,
            'stderr_events_enabled': stderr_events_enabled,
            'stderr_syslog': stderr_syslog,
            'environment': environment,
            'serverurl': serverurl,
            'directory': directory
        }
        with open(split_config_path(pid) + process_full_name + '.ini', 'w') as config_file:
            config.write(config_file)
        reread_and_update()
        return True



# render config file
def renderConfig(process_name):
    # remove the part after the '_' in the process_name and both the '_' 
    if (os.path.isfile(split_config_path() + process_name + '.ini')):
        # return the .ini file with dictionary format and omit the [program:process_name] header
        config = configparser.ConfigParser(interpolation=None)
        config.read(split_config_path() + process_name + '.ini')
        return dict(config.items('program:' + process_name))

    else:
        return 'File not found'
    
    
poly_visor = PolyVisor({"config_file": configPolyvisorPath()})  
poly_visor.refresh()


# get multiple supervisord instance 
def getMultipleSupervisors():
    supervisors = poly_visor.get_supervisors

    return supervisors


# get supervisord instance by uid
def getSupervisor(uid):
    
    poly_visor.refresh()
    supervisor = poly_visor.get_supervisor(uid)

    return supervisor


# get supervisord's processes by uid
def getSupervisorProcesses(uid):
    
    supervisor = poly_visor.get_supervisor_processes(uid)
    # poly_visor.refresh()

    return supervisor

# shutdown supervisord instance by uid

def shutdownSupervisors(*names):
    
    poly_visor.shutdown_supervisors(*names)

    return True

# restart supervisord instance by names
def restartSupervisors(*names):
   
    result = poly_visor.restart_supervisors(*names)

    return result

# start process by name




