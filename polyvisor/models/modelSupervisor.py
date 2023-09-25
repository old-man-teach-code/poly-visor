import time
from xmlrpc.client import ServerProxy
import sys
import os
from gevent import sleep, spawn
import  zerorpc
from polyvisor.controllers.utils import parse_dict, sanitize_url
import logging
import time

from blinker import signal

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser


# Get parent path of project to import modules
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
# insert into PYTHONPATH
sys.path.insert(1, parent)
from finder import serverURL

server = 'ServerProxy("http://localhost"+str(serverURL())+"/RPC2")'
import logging

log = logging.getLogger("polyvisor")

class Supervisor(dict):

    Null = {
        "identification": None,
        "api_version": None,
        "version": None,
        "supervisor_version": None,
        "processes": {},
        "running": False,
        "pid": None,
    }

    def __init__(self, name, url):
        super(Supervisor, self).__init__(self.Null)
        self.name = self["name"] = name
        self.url = self["url"] = url
        self.log = log.getChild(name)
        addr = sanitize_url(url, protocol="http", host=name, port=9002)
        self.address = addr["url"]
        self.host = self["host"] = addr["host"]
        self.server = ServerProxy(self.address + "/RPC2")
        print('Server, ', self.server)
        # fill supervisor info before events start coming in
        self.event_loop = spawn(self.run)

    def __repr__(self):
        return "{}(name={})".format(self.__class__.__name__, self.name)

    def __eq__(self, other):
        this, other = dict(self), dict(other)
        this_p = this.pop("processes")
        other_p = other.pop("processes")
        return this == other and list(this_p.keys()) == list(other_p.keys())

    def run(self):
        last_retry = time.time()
        while True:
            try:
                self.log.info("(re)initializing...")
                self.refresh()
                for i, event in enumerate(self.server.event_stream()):
                    # ignore first event. It serves only to trigger
                    # connection and avoid TimeoutExpired
                    if i != 0:
                        self.handle_event(event)
            except Exception as err:
                self.log.warning("Unexpected error %r", err)
            finally:
                curr_time = time.time()
                delta = curr_time - last_retry
                if delta < 10:
                    sleep(10 - delta)
                last_retry = time.time()

    def handle_event(self, event):
        name = event["eventname"]
        self.log.info("handling %s...", name)
        if name.startswith("SUPERVISOR_STATE"):
            self.refresh()
        elif not self["running"]:
            self.refresh()
        elif name.startswith("PROCESS_GROUP"):
            self.refresh()
        elif name.startswith("PROCESS_STATE"):
            payload = event["payload"]
            puid = "{}:{}:{}".format(
                self.name, payload["groupname"], payload["processname"]
            )
            self["processes"][puid].handle_event(event)

    def create_base_info(self):
        return dict(self.Null, name=self.name, url=self.url, host=self.host)

    def read_info(self):
        from polyvisor.models.modelProcess import Process
        info = self.create_base_info()
        server = self.server.supervisor
        
        # get PID
        info["pid"] = server.getPID()
        info["running"] = True
        info["identification"] = server.getIdentification()
        info["api_version"] = server.getAPIVersion()
        info["supervisor_version"] = server.getSupervisorVersion()
        info["processes"] = processes = server.getAllProcessInfo()
        procInfo = server.getAllProcessInfo()
        # for proc in procInfo:
        #     process = Process(self, parse_dict(proc))
        #     processes[process["uid"]] = process
        return info

    def update_info(self, info):
        info = parse_dict(info)
        if self == info:
            this_p, info_p = self["processes"], info["processes"]
            if this_p != info_p:
                for name, process in info_p.items():
                    if process != this_p[name]:
                        send(process, "process_changed")
            self.update(info)
        else:
            self.update(info)
            send(self, "supervisor_changed")

    def refresh(self):
        try:
            info = self.read_info()
        except:
            info = self.create_base_info()
            raise
        finally:
            self.update_info(info)

    def update_server(self, group_names=()):
        server = self.server
        try:
            added, changed, removed = server.reloadConfig()[0]
        except zerorpc.RemoteError as rerr:
            error(rerr.msg)
            return

        # If any gnames are specified we need to verify that they are
        # valid in order to print a useful error message.
        if group_names:
            groups = set()
            for info in server.getAllProcessInfo():
                groups.add(info["group"])
            # New gnames would not currently exist in this set so
            # add those as well.
            groups.update(added)

            for gname in group_names:
                if gname not in groups:
                    self.log.debug("unknown group %s", gname)

        for gname in removed:
            if group_names and gname not in group_names:
                continue
            results = server.stopProcessGroup(gname)
            self.log.debug("stopped process group %s", gname)

            fails = [res for res in results if res["status"] == Faults.FAILED]
            if fails:
                self.log.debug("%s as problems; not removing", gname)
                continue
            server.removeProcessGroup(gname)
            self.log.debug("removed process group %s", gname)

        for gname in changed:
            if group_names and gname not in group_names:
                continue
            server.stopProcessGroup(gname)
            self.log.debug("stopped process group %s", gname)

            server.removeProcessGroup(gname)
            server.addProcessGroup(gname)
            self.log.debug("updated process group %s", gname)

        for gname in added:
            if group_names and gname not in group_names:
                continue
            server.addProcessGroup(gname)
            self.log.debug("added process group %s", gname)

        self.log.info("Updated %s", self.name)

    def _reread(self):
        return self.server.reloadConfig()

    def restart(self):
        # do a reread. If there is an error (bad config) inform the user and
        # and refuse to restart
        try:
            self._reread()
        except zerorpc.RemoteError as rerr:
            error("Cannot restart: {}".format(rerr.msg))
            return
        result = self.server.restart(timeout=30)
        if result:
            info("Restarted {}".format(self.name))
        else:
            error("Error restarting {}".format(self.name))

    def reread(self):
        try:
            added, changed, removed = self._reread()[0]
        except zerorpc.RemoteError as rerr:
            error(rerr.msg)
        else:
            info(
                "Reread config of {} "
                "({} added; {} changed; {} disappeared)".format(
                    self.name, len(added), len(changed), len(removed)
                )
            )

    def shutdown(self):
        result = self.server.supervisor.shutdown()
        if result:
            info("Shut down {}".format(self.name))
        else:
            error("Error shutting down {}".format(self.name))


def send(payload, event):
    event_signal = signal(event)
    return event_signal.send(event, payload=payload)


def notification(message, level):
    payload = dict(message=message, level=level, time=time.time())
    send(payload, "notification")


def info(message):
    notification(message, "INFO")


def warning(message):
    logging.warning(message)
    notification(message, "WARNING")


def error(message):
    logging.error(message)
    notification(message, "ERROR")

