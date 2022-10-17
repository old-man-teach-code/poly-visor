from machinestatus import server

#Start process with name
def proc_Start(name):
    result=server.supervisor.startProcess(name)
    if (result!=True):
        return "ERROR: Can't start "+name
    return name+" Started"

#Start ALL process listed in configuration file
def proc_StartAll():
    result= server.supervisor.startAllProcesses()
    if(result!=True):
        return "ERROR: Unable to execute!"
    return "All processes have been started!"

#Stop process by name
def proc_Stop(name):
    try:
         server.supervisor.stopProcess(name)
    except:         
        return "ERROR: Can't stop "+name    
    return name+" has been stoped!"

#Stop ALL processes
def proc_stopALL():   
    server.supervisor.stopAllProcesses()        
    return "All processes has been stoped"