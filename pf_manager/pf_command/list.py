import json
from texttable import Texttable

from pf_manager.pf_command.base import BaseCommand


class ListCommand(BaseCommand):
    def __init__(self, config):
        super(ListCommand, self).__init__(config)
        self.config_path = config.obj["config"]

    def run(self):
        f = open(self.config_path, 'r')
        json_data = json.load(f)
        rows = self.convert_ditionary_to_2d_array(json_data)
        table = Texttable()
        table.add_rows(rows)
        print(table.draw())
        f.close()
        pass

    def convert_ditionary_to_2d_array(self, json_data):
        # index
        header = ["name", "type", "local_port", "host_port", "remote_host", "ssh_server", "server_port"]
        body = []
        for name in json_data.keys():
            target = json_data[name]
            target_body = [name]
            for field in header:
                if field == "name":
                    continue
                if field in target:
                    target_body.append(target[field])
                else:
                    target_body.append("")
            body.append(target_body)
        body.insert(0, header)
        return body
