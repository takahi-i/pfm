import json
from pf_manager.pf_command.base import BaseCommand


class ParameterCommand(BaseCommand):
    def __init__(self, config):
        super(ParameterCommand, self).__init__(config)
        self.name = config.params["name"]

    def run(self):
        f = open('.pfm', 'r')
        json_data = json.load(f)
        setting = json_data[self.name]
        if setting["type"] == "L":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["local_port"], setting["remote_host"], setting["host_port"], setting["ssh_server"]))
        elif setting["type"] == "R":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["server_port"], setting["remote_host"], setting["host_port"], setting["ssh_server"]))
        else:
            raise RuntimeError("Nothing type as " + setting["type"])
