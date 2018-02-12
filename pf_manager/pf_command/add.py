import json
import re
from pf_manager.pf_command.base import BaseCommand
from pf_manager.util.log import logger


def is_include_fields(target, fields):
    for field in fields:
        if field not in target or target[field] is None:
            raise RuntimeError("Field " + field + " is needed for port forwarding")


def check_fields(target):
    if target["type"] == "L":
        is_include_fields(target, AddCommand.LOCAL_FORWARDING_MUST_HAVE_FIELDS)
    elif target["type"] == "R":
        is_include_fields(target, AddCommand.REMOTE_FORWARDING_MUST_HAVE_FIELDS)
    else:
        raise RuntimeError("No forward type as " + target["type"])


def check_local_port_is_used(local_port, targets):
    for target_name in targets:
        target = targets[target_name]
        if local_port == target["local_port"]:
            logger.warn("local port {} is already used in {}".format(str(local_port), target_name))


def check_remote_port_is_used(new_target, targets):
    remote_port = new_target["remote_port"]
    remote_host = get_remote_host(new_target)

    for target_name in targets:
        target = targets[target_name]
        target_remote_host = get_remote_host(target)

        if target_remote_host == remote_host and target["remote_port"] == remote_port:
            logger.warn("remote port {} in host {} is already used in {} ".format(
                str(remote_port), remote_host, target_name))


def get_remote_host(target):
    target_remote_host = target["remote_host"]
    if target_remote_host == "localhost":
        target_remote_host = target["ssh_server"]
    return target_remote_host


def automatic_local_port_assignment(new_target, targets):
    if new_target["local_port"] is None:
        logger.info("local_port is not specified")
        logger.info("allocating local_port for " + new_target["name"] + "...")
        used_ports = set()
        for target_name in targets:
            used_ports.add(targets[target_name]["local_port"])

        for port_number in range(AddCommand.PFM_BASE_PORT, AddCommand.PFM_MAX_INFERRING_PORT, 1):
            if not str(port_number) in used_ports:
                new_target["local_port"] = str(port_number)
                logger.info("local_port of " + new_target["name"] + " is set to " + str(port_number))
                return


def automatic_remote_port_assignment(new_target, targets):
    if new_target["remote_port"] is None:
        logger.info("remote_port is not specified")
        logger.info("allocating remote_port for " + new_target["name"] + "...")
        remote_server_name = get_remote_host(new_target)

        used_ports = set()
        for target_name in targets:
            target = targets[target_name]
            if target["remote_host"] == remote_server_name:
                used_ports.add(target["remote_port"])
            if target["remote_host"] == "localhost" and target["ssh_server"] == remote_server_name:
                used_ports.add(target["remote_port"])
            if target["ssh_server"] == remote_server_name and target["server_port"] is not None:
                used_ports.add(target["server_port"])

        for port_number in range(AddCommand.PFM_BASE_PORT, AddCommand.PFM_MAX_INFERRING_PORT, 1):
            if not str(port_number) in used_ports:
                new_target["remote_port"] = str(port_number)
                logger.info("remote_port of " + new_target["name"] + " is set to " + str(port_number))
                return


class AddCommand(BaseCommand):
    DEFAULT_TYPE = "L"
    LOCAL_FORWARDING_MUST_HAVE_FIELDS = ["name", "remote_host", "remote_port", "local_port", "ssh_server"]
    REMOTE_FORWARDING_MUST_HAVE_FIELDS = ["name", "remote_host", "remote_port", "ssh_server", "server_port"]
    PFM_BASE_PORT = 49152
    PFM_MAX_INFERRING_PORT = 50152

    def __init__(self, name, ssh_param_str, forward_type,
                 remote_host, remote_port, local_port,
                 ssh_server, server_port, login_user, config):
        super(AddCommand, self).__init__(config)
        self.name = name
        self.ssh_param_str = ssh_param_str

        if forward_type is None:
            logger.info("No port forward type is specified")
            self.forward_type = AddCommand.DEFAULT_TYPE
        else:
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
        new_target = self.generate_consistent_target(targets)
        targets[self.name] = new_target
        f.close()

        # write the target
        f = open(self.config_path, 'w')
        f.write(json.dumps(targets, indent=4))
        f.close()

    def generate_consistent_target(self, targets):
        new_target = self.generate_target()
        automatic_local_port_assignment(new_target, targets)
        automatic_remote_port_assignment(new_target, targets)
        check_local_port_is_used(new_target["local_port"], targets)
        check_remote_port_is_used(new_target, targets)
        check_fields(new_target)
        return new_target

    def generate_target(self):
        new_target = self.__extract_target_from_params()
        if self.ssh_param_str is not None:
            logger.info("found argument...")
            new_target = self.__generate_target_from_argument(new_target)
        return new_target

    def __extract_target_from_params(self):
        target = {
            "type": self.forward_type, "remote_host": self.remote_host, "name": self.name,
            "remote_port": self.remote_port, "ssh_server": self.ssh_server,
            "login_user": self.login_user, "local_port": self.local_port,
            "server_port": self.server_port
        }
        return target

    def __generate_target_from_argument(self, target):
        first_port, remote_host, second_port, login_user, ssh_server = self.__parse(self.ssh_param_str)

        target["remote_host"] = remote_host
        target["ssh_server"] = ssh_server
        target["login_user"] = login_user

        if target["type"] == "L":
            target["local_port"] = first_port
            target["remote_port"] = second_port
        elif self.forward_type == "R":
            target["server_port"] = first_port
            target["remote_port"] = second_port

        return target

    def __parse(self, ssh_param_str):
        if ssh_param_str.count('@'):
            m = re.match(r'^(\d+):(.+):(\d+) +(.+)@(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        else:
            m = re.match(r'^(\d+):(.+):(\d+) +(.+)$', ssh_param_str)
            return m.group(1), m.group(2), m.group(3), None, m.group(4)
