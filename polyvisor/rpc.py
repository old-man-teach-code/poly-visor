from supervisor.rpcinterface import SupervisorNamespaceRPCInterface
from gevent.pywsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
import multiprocessing
from polyvisor.app import app

# ab = supervisord.Supervisor()
# polyVi = SupervisorNamespaceRPCInterface(ab)

def make_rpc_interface(supervisord,**config):    
    sup = SupervisorNamespaceRPCInterface(supervisord)
    
    #p1=threading.Thread(target=run_server)
    get_bind = config.get("bind",0)
    bind = int(get_bind)
    if(bind==0):
        bind=5000
    p1=multiprocessing.Process(target=run_server,args=(bind,))    
    p1.start()
    

def run_server(bind):   
    http_server = WSGIServer(("localhost", bind), app)
    http_server.serve_forever()