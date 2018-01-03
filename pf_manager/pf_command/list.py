import json

from texttable import Texttable

from pf_manager.pf_command.base import BaseCommand
from pf_manager.util.util import convert_dictionary_to_2d_array


class ListCommand(BaseCommand):
    def __init__(self, config):
        super(ListCommand, self).__init__(config)

    def run(self):
        f = open(self.config_path, 'r')
        json_data = json.load(f)
        rows = convert_dictionary_to_2d_array(json_data)
        table = Texttable()
        table.set_cols_align(["l", "l", "l", "l", "l", "l", "l", "l"])
        table.set_cols_width([20,  10,  10,  30,  10,  15,  30,  12])
        table.add_rows(rows)
        print(table.draw())
        f.close()
