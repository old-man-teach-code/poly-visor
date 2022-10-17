from models.modelProcess import Process
from models.modelSupervisor import Supervisor
# return a list of Process objects with all the attributes
def process_AllInfo():
    return Process.getAllProcessInfo()

def supervisor_State():
    return Supervisor.getSupervisorState()

processList = process_AllInfo()
for process in processList: 
    print(process.description)    
print('---------------')
supervisorInstance = supervisor_State()
print(supervisorInstance.statecode)
