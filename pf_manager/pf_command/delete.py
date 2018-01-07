import json

from pf_manager.pf_command.base import BaseCommand
from pf_manager.util.log import logger


class DeleteCommand(BaseCommand):
    def __init__(self, config, name):
        super(DeleteCommand, self).__init__(config)
        self.name = name

    def run(self):
        f = open(self.config_path, 'r')
        targets = json.load(f)
        if self.name in targets:
            targets.pop(self.name)
            logger.info('Deleted target ' + self.name + '...')
        else:
            logger.warn("Port forward setting named " + self.name + "is not registered")
        f.close()

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(targets, indent=4))
        f.close()
