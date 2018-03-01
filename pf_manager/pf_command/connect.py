import sys
import subprocess
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from pf_manager.pf_command.param import ParameterCommand


class ConnectCommand(ParameterCommand):

    def __init__(self, config, name):
        super(ConnectCommand, self).__init__(config, name)

    def run(self):
        ssh_param = self.__get_param()
        cmd = "ssh -A {}".format(ssh_param)
        subprocess.call(cmd, shell=True)

    def __get_param(self):
        buffer = StringIO()
        sys.stdout = buffer
        super(ConnectCommand, self).run()
        sys.stdout = sys.__stdout__
        ssh_param = buffer.getvalue()

        return ssh_param
