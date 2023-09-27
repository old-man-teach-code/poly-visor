

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

import fnmatch
from gevent import spawn, joinall
from polyvisor.finder import MultiOrderedDict, get_pid, runShell
from polyvisor.models.modelProcess import Process
from polyvisor.models.modelSupervisor import Supervisor
import os
import re
import configparser

def load_config(config_file):
    parser = configparser.RawConfigParser(
        dict_type=MultiOrderedDict, strict=False)
    parser.read(config_file)
    dft_global = dict(name="polyvisor")

    supervisors = {}
    config = dict(dft_global, supervisors=supervisors)
    # config.update(parser.items("global"))
    tasks = []
    for section in parser.sections():
        if not section.startswith("supervisor:"):
            continue
        name = section[len("supervisor:") :]
        section_items = dict(parser.items(section))
        url = section_items.get("url", "")
        supervisors[name] = Supervisor(name, url)
        
        
    return config


class PolyVisor(object):
    def __init__(self, options):
        self.options = options
        self.reload()

    @property
    def config(self):
        if self._config is None:
            try:
                
                self._config = load_config(self.options.get('config_file', ''))
            except Exception as e:
                print(f"Error loading configuration: {str(e)}")
                return None
          
        return self._config


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


    # 
    
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

    def stop_all_processes(self):
        self._do_processes(Process.stopAll, "*")

    def start_all_processes(self):
        self._do_processes(Process.startAll, "*")
    def stop_processes(self, *patterns):
        self._do_processes(Process.stop, *patterns)
        
    def start_processes(self, *patterns):
        self._do_processes(Process.start, *patterns)    


def filter_patterns(names, patterns):
    patterns = [
        "*:{}".format(p) if ":" not in p and "*" not in p else p for p in patterns
    ]
    result = set()
    sets = (fnmatch.filter(names, pattern) for pattern in patterns)
    list(map(result.update, sets))
    return result
