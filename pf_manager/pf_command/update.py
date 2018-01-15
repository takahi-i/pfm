import json

from pf_manager.pf_command.base import BaseCommand
from pf_manager.util.log import logger


class UpdateCommand(BaseCommand):
    def __init__(self, name, forward_type,
                 remote_host, remote_port, local_port,
                 ssh_server, server_port, login_user, config):
        super(UpdateCommand, self).__init__(config)
        self.name = name
        self.forward_type = forward_type
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_port = local_port
        self.ssh_server = ssh_server
        self.server_port = server_port
        self.login_user = login_user

    def run(self):
        f = open(self.config_path, 'r')
        targets = json.load(f)
        if self.name in targets:
            target = targets[self.name]
            self.update(target)
        else:
            logger.warn("Port forward setting named " + self.name + "is not registered")

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(targets, indent=4))
        f.close()

    def update(self, target):
        if self.forward_type is not None:
            target["type"] = self.forward_type
        if self.remote_host is not None:
            target["remote_host"] = self.remote_host
        if self.remote_port is not None:
            target["remote_port"] = self.remote_port
        if self.local_port is not None:
            target["local_port"] = self.local_port
        if self.ssh_server is not None:
            target["ssh_server"] = self.ssh_server
        if self.server_port is not None:
            target["server_port"] = self.server_port
        if self.login_user is not None:
            target["login_user"] = self.login_user
