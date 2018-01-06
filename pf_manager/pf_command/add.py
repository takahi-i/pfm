import json
import re
from pf_manager.pf_command.base import BaseCommand
from pf_manager.util.log import logger


class AddCommand(BaseCommand):

    DEFAULT_TYPE = "L"

    def __init__(self, config):
        super(AddCommand, self).__init__(config)
        self.params = config.params
        self.ssh_param_str = config.params.get("ssh_argument", None)
        self.forward_type = config.params.get("forward_type", AddCommand.DEFAULT_TYPE)
        self.remote_host = config.params.get("remote_host", None)
        self.remote_port = config.params.get("remote_port", None)
        self.name = config.params.get("name", None)
        self.local_port = self.params.get("local_port", None)
        self.ssh_server = self.params.get("ssh_server", None)
        self.login_user = self.params.get("login_user", None)

    def run(self):
        f = open(self.config_path, 'r')
        targets = json.load(f)
        new_target = self.__extract_target_from_params()
        if self.ssh_param_str is not None:
            logger.info("found argument...")
            new_target = self.__generate_from_argument(new_target)
        targets[self.name] = new_target
        f.close()

        # TODO: validate generated target

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(targets, indent=4))
        f.close()

    def __extract_target_from_params(self):
        target = {
            "type": self.forward_type, "remote_host": self.remote_host, "name": self.name,
            "remote_port": self.remote_port, "ssh_server": self.ssh_server
        }
        if "login_user" in self.params:
            target["login_user"] = self.login_user

        if self.params["forward_type"] == 'L':
            target["local_port"] = self.local_port
        elif self.params["forward_type"] == 'R':
            target["server_port"] = self.local_port
        else:
            raise RuntimeError("No such port forwarding type as " + self.params["forward_type"])
        return target

    def __generate_from_argument(self, target):
        first_port, remote_host, second_port, login_user, ssh_server = self.__parse(self.ssh_param_str)

        target["remote_host"] = remote_host
        target["ssh_server"] = ssh_server
        target["login_user"] = login_user

        if target["type"] == "L":
            target["local_port"] = first_port
            target["remote_port"] = second_port
        elif self.params["forward_type"] == "R":
            target["server_port"] = first_port
            target["remote_port"] = second_port
        else:
            raise RuntimeError("No type as " + self.params["forward_type"])

        return target

    def __parse(self, ssh_param_str):
        if ssh_param_str.count('@'):
            m = re.match(r'^(\d+):(.+):(\d+) +(.+)@(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        else:
            m = re.match(r'^(\d+):(.+):(\d+) +(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3), None, m.group(4)
