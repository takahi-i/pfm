import json

from pf_manager.pfm_command.base import BaseCommand


class ListCommand(BaseCommand):
    def run(self):
        f = open('data.json', 'r')
        jsonData = json.load(f)
        print(json.dumps(jsonData, sort_keys = True, indent = 4))
        f.close()
        pass
