import json

from pf_manager.pf_command.base import BaseCommand


class ListCommand(BaseCommand):
    def __init__(self, config):
        super(ListCommand, self).__init__(config)
        self.config_path = config.obj["config"]

    def run(self):
        f = open(self.config_path, 'r')
        json_data = json.load(f)
        print(json.dumps(json_data, sort_keys=True, indent=4))
        f.close()
        pass
