import json
from pf_manager.pf_command.base import BaseCommand


class ParameterCommand(BaseCommand):
    def __init__(self, config, name):
        super(ParameterCommand, self).__init__(config)
        self.name = name

    def run(self):
        f = open(self.config_path, 'r')
        json_data = json.load(f)
        setting = json_data[self.name]
        if setting["type"] == "L":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["local_port"], setting["remote_host"],
                                                setting["remote_port"], self.__server_param(setting)))
        elif setting["type"] == "R":
            print("-{0} {1}:{2}:{3} {4}".format(setting["type"], setting["server_port"], setting["remote_host"],
                                                setting["remote_port"], self.__server_param(setting)))
        else:
            raise RuntimeError("Nothing type as " + setting["type"])

    def __server_param(self, setting):
        if setting["login_user"] is None or setting["login_user"] == "":
            return setting["ssh_server"]
        else:
            return setting["login_user"] + "@" + setting["ssh_server"]
