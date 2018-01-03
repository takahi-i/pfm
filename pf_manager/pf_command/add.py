import json
import re
from pf_manager.pf_command.base import BaseCommand
from pf_manager.util.log import logger


class AddCommand(BaseCommand):
    def __init__(self, config):
        super(AddCommand, self).__init__(config)
        self.params = config.params
        self.ssh_param_str = config.params["ssh_param"]
        self.name = config.params["name"]
        self.config_path = config.obj["config"]

    def run(self):
        f = open(self.config_path, 'r')
        targets = json.load(f)
        if self.params["ssh_server"] is not None:
            logger.info("Register target from params...")
            targets[self.name] = self.__extract_target_from_params()
        elif self.ssh_param_str is not None:
            logger.info("Register target from argument string...")
            self.__generate_from_string(targets)
        else:
            raise RuntimeError("given parameters are invalid: " + str(self.params))
        f.close()

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(targets, indent=4))
        f.close()

    def __extract_target_from_params(self):
        target = {
            "type": self.params["forward_type"], "remote_host": self.params["remote_host"],
            "host_port": self.params["host_port"], "ssh_server": self.params["ssh_server"]
        }

        if "login_user" in self.params:
            target["login_user"] = self.params["login_user"]

        if self.params["forward_type"] == 'L':
            target["local_port"] = self.params["local_port"]
        elif self.params["forward_type"] == 'R':
            target["server_port"] = self.params["local_port"]
        else:
            raise RuntimeError("No such port forwarding type as " + self.params["forward_type"])
        return target

    def __generate_from_string(self, json_data):
        forward_type, first_port, host, second_port, login_user, ssh_server = self.__parse(self.ssh_param_str)
        if forward_type == "L":
            json_data[self.name] = {"type": forward_type, "remote_host": host, "ssh_server": ssh_server,
                                    "local_port": first_port, "host_port": second_port, "login_user": login_user}
        elif forward_type == "R":
            json_data[self.name] = {"type": forward_type, "remote_host": host, "ssh_server": ssh_server,
                                    "server_port": first_port, "host_port": second_port, "login_user": login_user}
        else:
            raise RuntimeError("No type as " + forward_type)


    def __parse(self, ssh_param_str):
        if ssh_param_str.count('@'):
            m = re.match(r'^([RL]) ?(\d+):(.+):(\d+) +(.+)@(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3),m.group(4), m.group(5), m.group(6)
        else:
            m = re.match(r'^([RL]) ?(\d+):(.+):(\d+) +(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3),m.group(4), "", m.group(5)
