from modelSupervisor import server


class Process:
    name = ""
    group = ""
    description = ""
    start = ""
    stop = ""
    state = ""
    statename = ""
    spawnerr = ""
    exitstatus = ""
    logfile = ""
    stdout_logfile = ""
    stderr_logfile = ""
    pid = 0

    def __init__(self, name, group,  start, stop, state, statename, spawnerr, exitstatus, logfile, stdout_logfile, stderr_logfile, pid, description):
        self.name = name
        self.group = group
        self.start = start
        self.stop = stop
        self.state = state
        self.statename = statename
        self.spawnerr = spawnerr
        self.exitstatus = exitstatus
        self.logfile = logfile
        self.stdout_logfile = stdout_logfile
        self.stderr_logfile = stderr_logfile
        self.pid = pid
        self.description = description

    @classmethod
    def getAllProcessInfo(self):
        # get all process info from supervisor and return a list of Process objects
        processInfo = server.supervisor.getAllProcessInfo()

        processList = []
        for process in processInfo:
            processList.append(Process(
                process['name'],
                process['group'],
                process['start'],
                process['stop'],
                process['state'],
                process['statename'],
                process['spawnerr'],
                process['exitstatus'],
                process['logfile'],
                process['stdout_logfile'],
                process['stderr_logfile'],
                process['pid'],
                process['description']))

            print(process['name'])

        return processList



   
    # create get set method for each attribute

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getGroup(self):
        return self.group

    def setGroup(self, group):
        self.group = group

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getStart(self):
        return self.start

    def setStart(self, start):
        self.start = start

    def getStop(self):
        return self.stop

    def setStop(self, stop):
        self.stop = stop

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getStateName(self):
        return self.statename

    def setStateName(self, statename):
        self.statename = statename

    def getSpawnErr(self):
        return self.spawnerr

    def setSpawnErr(self, spawnerr):
        self.spawnerr = spawnerr

    def getExitStatus(self):
        return self.exitstatus

    def setExitStatus(self, exitstatus):
        self.exitstatus = exitstatus

    def getLogFile(self):
        return self.logfile

    def setLogFile(self, logfile):
        self.logfile = logfile

    def getStdoutLogFile(self):
        return self.stdout_logfile

    def setStdoutLogFile(self, stdout_logfile):
        self.stdout_logfile = stdout_logfile

    def getStderrLogFile(self):
        return self.stderr_logfile

    def setStderrLogFile(self, stderr_logfile):
        self.stderr_logfile = stderr_logfile


# start all processes, return array result
def startAllProcesses():
    return server.supervisor.startAllProcesses()

# start process by name, always return True unless error
def startProcessByName(name):
    return server.supervisor.startProcess(name)

# stop process by name, always return True unless error
def stopProcessByName(name):
    return server.supervisor.stopProcess(name)

# stop all process, return array result
def stopAllProcesses():
    return server.supervisor.stopAllProcesses()

#return all data from stdOut in logfile of process with name
def allData_stdOut_logFile(name):
    return server.supervisor.readProcessStdoutLog(name,0,0)

#return all data from stdErr in logfile of process with name
def allData_stdErr_logFile(name):
    return server.supervisor.readProcessStderrLog(name,0,0)

#clear process stdOut,stdErr log by name, always return True unless error
def clear_process_log(name):
    return server.supervisor.clearProcessLogs(name)
