from finder import get_sup_serverurl
from xmlrpc.client import ServerProxy
server = ServerProxy("http://localhost"+str(get_sup_serverurl())+"/RPC2")


class Supervisor:
    statecode = 0
    statename = ""

    def __init__(self, statecode, statename):
        self.statecode = statecode
        self.statename = statename

    @classmethod
    def getSupervisorState(self):
        state = server.supervisor.getState()
        return Supervisor(state['statecode'], state['statename'])