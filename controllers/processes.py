import sys
sys.path.insert(0,'//wsl$/Ubuntu/root/new/poly-visor/models/modelProcess.py')
from models.modelProcess import Process

#get all processes
def get_all_processes():
    return Process.getAllProcessInfo()