import re
from pf_manager.pf_command.base import BaseCommand


class AddCommand(BaseCommand):
    def __init__(self, config):
        super(AddCommand, self).__init__(config)
        self.ssh_param_str = config.params["ssh_param"]
        self.name = config.params["name"]

    def run(self):
        self.__parse(self.ssh_param_str)

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
