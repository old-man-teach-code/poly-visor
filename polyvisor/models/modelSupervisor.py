import configparser
import time
from xmlrpc.client import ServerProxy
import sys
import os
from gevent import sleep, spawn
import requests
import  zerorpc
from polyvisor.controllers.utils import parse_dict, sanitize_url, send_webhook_alert
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
from finder import configPolyvisorPath, serverURL

server = 'ServerProxy("http://localhost"+str(serverURL())+"/RPC2")'
import logging

log = logging.getLogger("polyvisor")

# The Supervisor class is defined, inheriting from the built-in dict class.
# It represents a supervisor entity with attributes such as processes, running status, PID, and authentication.
class Supervisor(dict):

    # Default null values for a supervisor entity.
    Null = {
        "processes": {},
        "running": False,
        "pid": None,
        "authentication": False,
    }

    # Constructor for Supervisor class.
    def __init__(self, name, url, webhook_url=None):
        super(Supervisor, self).__init__(self.Null)
        self.name = self["name"] = name
        self.url = self["url"] = url
        self.log = log.getChild(name)

        # Sanitize the URL, set the address, host, and create a ServerProxy for communication.
        addr = sanitize_url(url, protocol="http", host=name, port=9002)
        self.address = addr["url"]
        self.host = self["host"] = addr["host"]
        self.webhook_url = webhook_url
        self.server = ServerProxy(self.address + "/RPC2")

        # Spawn the event loop to run the 'run' method asynchronously.
        self.event_loop = spawn(self.run)

    # String representation of the Supervisor object.
    def __repr__(self):
        return "{}(name={})".format(self.__class__.__name__, self.name)

    # Equality comparison method for two Supervisor objects.
    def __eq__(self, other):
        this, other = dict(self), dict(other)
        this_p = this.pop("processes")
        other_p = other.pop("processes")
        return this == other and list(this_p.keys()) == list(other_p.keys())

    # Asynchronous method to run the Supervisor event loop.
    async def run(self):
        last_retry = time.time()
        while True:
            try:
                self.log.info("(re)initializing...")
                self.refresh()

                # Assuming you have an async method to get events
                events = await self.server.get_events()

                for i, event in enumerate(events):
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

    # Method to handle supervisor events and trigger the corresponding actions.
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

    # Method to create the base information dictionary for the supervisor.
    def create_base_info(self):
        return dict(self.Null, name=self.name, url=self.url, host=self.host)

    # Method to read detailed information about the supervisor.
    def read_info(self):
        from polyvisor.models.modelProcess import Process

        info = self.create_base_info()

        server = self.server.supervisor

        # get PID
        info["pid"] = server.getPID()
        info["running"] = True

        info["authentication"] = self.check_authentication()

        info["processes"] = processes = {}
        procInfo = server.getAllProcessInfo()
        for proc in procInfo:
            process = Process(self, parse_dict(proc))
            processes[process["uid"]] = process
        return info

    # Method to check if authentication is required for the supervisor.
    def check_authentication(self):
        file_location = configPolyvisorPath()
        authentication_required = False
        config = configparser.ConfigParser()
        # read the file
        config.read(file_location)
        for section in config.sections():
            if section.startswith("supervisor:{}".format(self.name)):
                username = config.get(section, 'username', fallback=None)
                password = config.get(section, 'password', fallback=None)

                if username and password:
                    authentication_required = True
                    break  # Authentication is required in at least one section, no need to continue checking
                else:
                    authentication_required = False
                    break

        return authentication_required

    # Method to get detailed information about the supervisor's processes.
    def get_processes(self):
        from polyvisor.models.modelProcess import Process
        info = self.create_base_info()

        server = self.server.supervisor

        # get PID
        info["pid"] = server.getPID()
        info["running"] = True
        info["authentication"] = True
        info["processes"] = processes = {}
        procInfo = server.getAllProcessInfo()
        for proc in procInfo:
            process = Process(self, parse_dict(proc))
            processes[process["uid"]] = process
        return info

    # Method to update supervisor information based on the provided info.
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

    # Method to refresh the supervisor by reading and updating its information.
    def refresh(self):
        try:
            info = self.read_info()
        except:
            info = self.create_base_info()
            raise
        finally:
            self.update_info(info)

    # Method to update the server by reloading its configuration and performing necessary actions.
    def update_server(self, group_names=()):
        server = self.server.supervisor
        try:
            added, changed, removed = server.reloadConfig()[0]
        except zerorpc.RemoteError as rerr:
            error(rerr.msg)
            return

        # If any group names are specified, verify their validity to print a useful error message.
        if group_names:
            groups = set()
            for info in server.getAllProcessInfo():
                groups.add(info["group"])
            # New group names would not currently exist in this set, so add those as well.
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
                self.log.debug("%s has problems; not removing", gname)
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

    # Method to reread the supervisor's configuration.
    def _reread(self):
        return self.server.supervisor.reloadConfig()

    # Method to restart the supervisor.
    def restart(self):
        # Perform a reread. If there is an error (bad config), inform the user and refuse to restart.
        self._reread()

        result = self.server.supervisor.restart()
        if result:
            info("Restarted {}".format(self.name))
            send_webhook_alert(self.webhook_url, "Restarted {}".format(self.name))
            return "Restarted {}".format(self.name)
        else:
            error("Error restarting {}".format(self.name))
            return "Error restarting {}".format(self.name)

    # Method to reread the supervisor's configuration.
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

    # Method to shut down the supervisor.
    def shutdown(self):
        result = self.server.supervisor.shutdown()
        if result:
            send_webhook_alert(self.webhook_url, "Shutdown {}".format(self.name))
            info("Shut down {}".format(self.name))
            return "Shut down {}".format(self.name)
        else:
            error("Error shutting down {}".format(self.name))
            return "Error shutting down {}".format(self.name)

# Helper function to send an event payload with a specific event signal.
def send(payload, event):
    event_signal = signal(event)
    return event_signal.send(event, payload=payload)

# Helper function to send a notification with a specific message and level.
def notification(message, level):
    payload = dict(message=message, level=level, time=time.time())
    send(payload, "notification")

# Helper functions for logging INFO, WARNING, and ERROR messages along with notifications.
def info(message):
    notification(message, "INFO")

def warning(message):
    logging.warning(message)
    notification(message, "WARNING")

def error(message):
    logging.error(message)
    notification(message, "ERROR")
