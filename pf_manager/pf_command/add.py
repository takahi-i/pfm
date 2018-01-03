import json
import re
from pf_manager.pf_command.base import BaseCommand


class AddCommand(BaseCommand):
    def __init__(self, config):
        super(AddCommand, self).__init__(config)
        self.ssh_param_str = config.params["ssh_param"]
        self.name = config.params["name"]
        self.config_path = config.obj["config"]

    def run(self):
        forward_type, first_port, host, second_port, ssh_server = self.__parse(self.ssh_param_str)

        # add port forwarding target
        f = open(self.config_path, 'r')
        json_data = json.load(f)
        if forward_type == "L":
            json_data[self.name] = {"type": forward_type, "remote_host":  host, "ssh_server": ssh_server, "local_port": first_port, "host_port": second_port}
        elif forward_type == "R":
            json_data[self.name] = {"type": forward_type, "remote_host":  host, "ssh_server": ssh_server, "server_port": first_port, "host_port": second_port}
        else:
            raise RuntimeError("No type as " + forward_type)
        f.close()

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(json_data, indent=4))
        f.close()

        print(self.ssh_param_str)

    def __parse(self, ssh_param_str):
        print("parsing:" + ssh_param_str)
        m = re.match(r'^([RL]) ?(\d+):(.+):(\d+) (.+)$', ssh_param_str)
        forward_type = m.group(1)
        first_port = m.group(2)
        host = m.group(3)
        second_port = m.group(4)
        ssh_server = m.group(5)
        return forward_type, first_port, host, second_port, ssh_server
