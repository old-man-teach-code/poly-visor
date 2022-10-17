from machinestatus import server

#Clear log of supervisord
def sup_clearLog():
    server.supervisor.clearLog()

#Shutdown Supervisord process
def sup_shutdown():
    result=server.supervisor.shutdown()
    if(result!= True):
        return "ERROR: Shutdown operation is failed!"
    return "Supervisord is shutdown!"

#Restart Supervisord process
def sup_restart():
    result=server.supervisor.restart()
    if(result!=True):
        return "ERROR: Can't restart supervisord"
    return "Supervisord restarted successfully!"
   
print(sup_restart())