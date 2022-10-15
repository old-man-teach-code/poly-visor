import sys
sys.path.insert(0,'//wsl$/Ubuntu/root/new/poly-visor/models/modelSupervisor.py')
from models.modelSupervisor import Supervisor


# get Supervisor object from modelSupervisor
def get_supervisor():
    a = Supervisor()
    return a
print(get_supervisor())