import json

from pf_manager.pf_command.base import BaseCommand


class ListCommand(BaseCommand):
    def run(self):
        f = open('.pfm', 'r')
        jsonData = json.load(f)
        print(json.dumps(jsonData, sort_keys = True, indent = 4))
        f.close()
        pass
