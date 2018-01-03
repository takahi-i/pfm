import json
from pf_manager.pf_command.base import BaseCommand


class ParameterCommand(BaseCommand):
    def __init__(self, config):
        super(ParameterCommand, self).__init__(config)
        self.name = config.params["name"]

    def run(self):
        f = open(self.config_path, 'r')
        json_data = json.load(f)
        setting = json_data[self.name]
        if setting["type"] == "L":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["local_port"], setting["remote_host"],
                                                setting["host_port"], self.__server_param(setting)))
        elif setting["type"] == "R":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["server_port"], setting["remote_host"],
                                                setting["host_port"], self.__server_param(setting)))
        else:
            raise RuntimeError("Nothing type as " + setting["type"])

    def __server_param(self, setting):
        if len(setting["login_user"]) == 0:
            return setting["ssh_server"]
        else:
            return setting["login_user"] + "@" + setting["ssh_server"]
