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
    get_bind = config.get("bind",5000)
    access_point = config.get("access_point","localhost")    
    if access_point == "auto":        
        access_point = get_ip()       
    bind = int(get_bind)   
    p1=multiprocessing.Process(target=run_server,args=(access_point,bind,))    
    p1.start()
    

def run_server(ipAddress,bind):   
    http_server = WSGIServer((ipAddress, bind), app)
    http_server.serve_forever()

def get_ip():
    try:
        import socket
        # get ipv4 and ipv6 address of machine using socket module
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipv4 = s.getsockname()[0]
        s.close()
        return ipv4
    except:
        return "localhost"