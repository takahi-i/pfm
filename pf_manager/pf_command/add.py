import json
import re
from pf_manager.pf_command.base import BaseCommand
from pf_manager.util.log import logger


class AddCommand(BaseCommand):
    DEFAULT_TYPE = "L"

    def __init__(self, name, ssh_param_str, forward_type, remote_host, remote_port, local_port, ssh_server, server_port, login_user,
                 config):
        super(AddCommand, self).__init__(config)
        self.name = name
        self.ssh_param_str = ssh_param_str
        self.forward_type = forward_type
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_port = local_port
        self.ssh_server = ssh_server
        self.server_port = server_port
        self.login_user = login_user

    def run(self):
        f = open(self.config_path, 'r')
        targets = json.load(f)
        targets[self.name] = self.generate_target()
        f.close()

        # TODO: validate generated target

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(targets, indent=4))
        f.close()

    def generate_target(self):
        new_target = self.__extract_target_from_params()
        if self.ssh_param_str is not None:
            logger.info("found argument...")
            new_target = self.__generate_target_from_argument(new_target)
        return new_target

    def __extract_target_from_params(self):
        target = {
            "type": self.forward_type, "remote_host": self.remote_host, "name": self.name,
            "remote_port": self.remote_port, "ssh_server": self.ssh_server
        }

        if self.login_user is not None and len(self.login_user) > 0:
            target["login_user"] = self.login_user

        if self.forward_type == 'L':
            target["local_port"] = self.local_port
        elif self.forward_type == 'R':
            target["server_port"] = self.local_port
        return target

    def __generate_target_from_argument(self, target):
        first_port, remote_host, second_port, login_user, ssh_server = self.__parse(self.ssh_param_str)

        target["remote_host"] = remote_host
        target["ssh_server"] = ssh_server
        target["login_user"] = login_user

        if target["type"] is None:
            logger.info("No port forward type is specified")
            logger.info("Set local type")
            target["type"] = AddCommand.DEFAULT_TYPE

        if target["type"] == "L":
            target["local_port"] = first_port
            target["remote_port"] = second_port
        elif self.forward_type == "R":
            target["server_port"] = first_port
            target["remote_port"] = second_port


        return target

    def __parse(self, ssh_param_str):
        if ssh_param_str.count('@'):
            m = re.match(r'^(\d+):(.+):(\d+) +(.+)@(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        else:
            m = re.match(r'^(\d+):(.+):(\d+) +(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3), None, m.group(4)
