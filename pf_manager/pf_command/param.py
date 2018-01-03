import json
import re
from pf_manager.pf_command.base import BaseCommand


class ParameterCommand(BaseCommand):
    def __init__(self, config):
        super(ParameterCommand, self).__init__(config)
        self.name = config.params["name"]

    def run(self):
        # add port forwarding target
        f = open('.pfm', 'r')
        json_data = json.load(f)
        setting = json_data[self.name]
        if setting["type"] == "L":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["local_port"], setting["remote_host"], setting["host_port"], setting["ssh_server"]))
        elif setting["type"] == "R":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["server_port"], setting["remote_host"], setting["host_port"], setting["ssh_server"]))
        else:
            raise RuntimeError("Nothing type as " + setting["type"])


    def __parse(self, ssh_param_str):
        print("parsing:" + ssh_param_str)
        m = re.match(r'^ssh\s+-([RL]) ?(\d+):(.+):(\d+) (.+)$', ssh_param_str)
        forward_type = m.group(1)
        first_port = m.group(2)
        host = m.group(3)
        second_port = m.group(4)
        ssh_server = m.group(5)

        print("type:" + forward_type)
        print("first_port: " + first_port)
        print("host: " + host)
        print("second_port: " + second_port)
        print("ssh_server:" + ssh_server)

        return forward_type, first_port, host, second_port, ssh_server
