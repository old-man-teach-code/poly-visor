

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

# This function loads the configuration from the specified config file.
# It uses the configparser module to parse the file, creating a dictionary structure.
# Default values for the global configuration and an empty dictionary for supervisors are defined.
# The function then iterates through the sections in the parsed configuration,
# creating Supervisor objects for sections starting with "supervisor:" and adding them to the supervisors dictionary.
# The final configuration dictionary is returned.
def load_config(config_file):
    parser = configparser.RawConfigParser(
        dict_type=MultiOrderedDict, strict=False)
    parser.read(config_file)
    dft_global = dict(name="polyvisor")

    supervisors = {}
    config = dict(dft_global, supervisors=supervisors)

    for section in parser.sections():
        if not section.startswith("supervisor:"):
            continue
        name = section[len("supervisor:") :]
        section_items = dict(parser.items(section))
        url = section_items.get("url", "")
        webhook_url = section_items.get("webhook_url", "")
        supervisors[name] = Supervisor(name, url, webhook_url)

    return config

# The PolyVisor class is defined, representing a higher-level interface for interacting with supervisors and processes.
# It utilizes the load_config function to load the configuration.
# Various properties and methods are defined for accessing and manipulating the configuration.
class PolyVisor(object):
    def __init__(self, options):
        self.options = options
        self.reload()

    # Property to get the configuration. If the configuration is not loaded, it attempts to load it.
    @property
    def config(self):
        if self._config is None:
            try:
                self._config = load_config(self.options.get('config_file', ''))
            except Exception as e:
                print(f"Error loading configuration: {str(e)}")
                return None
        return self._config

    # Property indicating whether authentication is required based on the configuration.
    @property
    def use_authentication(self):
        # Initialize as False and check if any supervisor section requires authentication.
        authentication_required = False
        config = configparser.ConfigParser()
        config.read_string(self.config_file_content)

        for section in config.sections():
            if section.startswith("supervisor:"):
                username = config.get(section, 'username', fallback=None)
                password = config.get(section, 'password', fallback=None)
                if username and password:
                    authentication_required = True
                    break

        return authentication_required

    # Method to check if a given login (username and password) is valid for a supervisor.
    def is_login_valid(self, supervisor_name, username, password):
        # Load the configuration and check if the provided login matches the supervisor's credentials.
        config = configparser.ConfigParser()
        config.read_string(self.config_file_content)
        section_name = f"supervisor:{supervisor_name}"

        if section_name in config:
            section_username = config.get(section_name, 'username', fallback=None)
            section_password = config.get(section_name, 'password', fallback=None)
            return username == section_username and password == section_password
        else:
            return False

    # Method to check if a given user is authorized for a supervisor.
    def is_user_authorized(self, supervisor_name, username):
        # Load the configuration and check if the provided username matches the supervisor's username.
        config = configparser.ConfigParser()
        config.read_string(self.config_file_content)
        section_name = f"supervisor:{supervisor_name}"

        if section_name in config:
            section_username = config.get(section_name, 'username', fallback=None)
            return username == section_username
        else:
            return False

    # Property to get the content of the configuration file.
    @property
    def config_file_content(self):
        with open(self.options.get('config_file', '')) as config_file:
            return config_file.read()

    # Method to reload the configuration.
    def reload(self):
        self._config = None
        return self.config

    # Property to get the supervisors from the configuration.
    @property
    def supervisors(self):
        return self.config["supervisors"]

    # Property to get a list of supervisor objects with additional "name" field.
    @property
    def get_supervisors(self):
        supervisors_dict = self.config["supervisors"]
        result_array = []

        for key, value in supervisors_dict.items():
            value["name"] = key
            result_array.append(value)

        return result_array
    def get_supervisor(self, name):
        return self.supervisors[name]
    def get_supervisor_processes(self, name):
        return self.supervisors[name].get_processes()


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

    # Property to get all processes from supervisors.
    @property
    def processes(self):
        procs = (svisor["processes"] for svisor in self.supervisors.values())
        return {puid: proc for sprocs in procs for puid, proc in sprocs.items()}

    # Method to refresh supervisors.
    def refresh(self):
        tasks = [spawn(supervisor.refresh) for supervisor in self.supervisors.values()]
        joinall(tasks)

    # Methods to perform various operations on supervisors and processes.
    # These methods use the _do_supervisors and _do_processes helper methods.
    # The _do_supervisors and _do_processes methods use the spawn function to perform operations concurrently.
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

    def stop_all_processes_by_supervisor(self, *names):
        self._do_processes(Process.stopAll, '*')

    def start_all_processes_by_supervisor(self, *names):
        self._do_processes(Process.startAll, '*')

    def stop_processes(self, *patterns):
        self._do_processes(Process.stop, *patterns)

    def start_processes(self, *patterns):
        self._do_processes(Process.start, *patterns)

# Function to filter patterns using fnmatch and create a set of matching names.
def filter_patterns(names, patterns):
    patterns = [
        "*:{}".format(p) if ":" not in p and "*" not in p else p for p in patterns
    ]
    result = set()
    sets = (fnmatch.filter(names, pattern) for pattern in patterns)
    list(map(result.update, sets))
    return result
