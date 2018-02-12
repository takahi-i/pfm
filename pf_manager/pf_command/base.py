from abc import abstractmethod

import os

from pf_manager.util.log import logger


class BaseCommand(object):
    def __init__(self, config_path):
        self.config_path = config_path

        if self.config_path is None:
            logger.info('config_path set to None...')
            logger.info('Skip creating setting file...')
            return

        if not os.path.exists(self.config_path):
            logger.info('Creating setting file of pfm in ' + self.config_path + '...')
            f = open(self.config_path, 'w')
            f.write('{}')
            f.close()

    @abstractmethod
    def run(self):
        pass
