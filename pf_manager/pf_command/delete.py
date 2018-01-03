import json

from pf_manager.pf_command.base import BaseCommand


class DeleteCommand(BaseCommand):
    def __init__(self, config):
        super(DeleteCommand, self).__init__(config)
        self.name = config.params["name"]
        self.config_path = config.obj["config"]

    def run(self):
        f = open(self.config_path, 'r')
        json_data = json.load(f)
        target = json_data.pop(self.name)
        f.close()

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(json_data, indent=4))
        f.close()
