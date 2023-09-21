import copy
import logging
import os
import time
import weakref

from blinker import signal

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

import zerorpc
from gevent import spawn, sleep, joinall
from supervisor.xmlrpc import Faults
from supervisor.states import RUNNING_STATES

from .util import sanitize_url, filter_patterns, parse_dict
class PolyVisor(object):
    def __init__(self, options):
        self.options = options
        self.reload()

    # @property
    # def config(self):
    #     if self._config is None:
    #         self._config = load_config(self.options.config_file)
    #     return self._config

    # @property
    # def safe_config(self):
    #     """
    #     :return: config dict without username and password
    #     """
    #     if not self.use_authentication:
    #         return self.config

    #     config = copy.copy(self.config)
    #     config.pop("username", "")
    #     config.pop("password", "")
    #     return config

    @property
    def config_file_content(self):
        with open(self.options.config_file) as config_file:
            return config_file.read()

    def reload(self):
        self._config = None
        return self.config

    @property
    def supervisors(self):
        return self.config["supervisors"]

    @property
    def processes(self):
        procs = (svisor["processes"] for svisor in self.supervisors.values())
        return {puid: proc for sprocs in procs for puid, proc in sprocs.items()}

    # @property
    # def use_authentication(self):
    #     """
    #     :return: whether authentication should be used
    #     """
    #     username = self.config.get("username", False)
    #     password = self.config.get("password", False)
    #     return bool(username and password)

    # @property
    # def secret_key(self):
    #     return os.environ.get("MULTIVISOR_SECRET_KEY")

    def refresh(self):
        tasks = [spawn(supervisor.refresh) for supervisor in self.supervisors.values()]
        joinall(tasks)

    def get_supervisor(self, name):
        return self.supervisors[name]

    def get_process(self, uid):
        supervisor, _ = uid.split(":", 1)
        return self.supervisors[supervisor]["processes"][uid]

    def _do_supervisors(self, operation, *names):
        supervisors = (self.get_supervisor(name) for name in names)
        tasks = [spawn(operation, supervisor) for supervisor in supervisors]
        joinall(tasks)

    def _do_processes(self, operation, *patterns):
        procs = self.processes
        puids = filter_patterns(procs, patterns)
        tasks = [spawn(operation, procs[puid]) for puid in puids]
        joinall(tasks)

    def update_supervisors(self, *names):
        self._do_supervisors(Supervisor.update_server, *names)

    def restart_supervisors(self, *names):
        self._do_supervisors(Supervisor.restart, *names)

    def reread_supervisors(self, *names):
        self._do_supervisors(Supervisor.reread, *names)

    def shutdown_supervisors(self, *names):
        self._do_supervisors(Supervisor.shutdown, *names)

    def restart_processes(self, *patterns):
        self._do_processes(Process.restart, *patterns)

    def stop_processes(self, *patterns):
        self._do_processes(Process.stop, *patterns)