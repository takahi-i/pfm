# -*- coding: utf-8 -*-

"""Console script for pfm."""

import click
from click import ClickException
import os

from pf_manager.pf_command.add import AddCommand
from pf_manager.pf_command.delete import DeleteCommand
from pf_manager.pf_command.list import ListCommand
from pf_manager.pf_command.param import ParameterCommand


class PFMGroup(click.Group):
    def invoke(self, ctx):
        ctx.obj = {}
        super(PFMGroup, self).invoke(ctx)


@click.group(cls=PFMGroup, help='port forwarding manager')
@click.option('-c', '--config', type=str, help="configuration file (DEFAULT $HOME/.pfm)")
@click.pass_context
def main(ctx, config):
    if ctx.params["config"] is None:
        ctx.obj['config'] = os.environ.get("HOME") + "/.pfm"
    else:
        ctx.obj['config'] = ctx.params["config"]


@main.command(help='add port forwarding target')
@click.pass_context
@click.option('-n', '--name', type=str, help="name of port fowarding", required=False)
@click.option('--forward_type', type=str, help="port forwarding type [L or R]", required=False, default='L')
@click.option('--local_port', type=int, help="local port", required=False)
@click.option('--host_port', type=int, help="remote host port", required=False)
@click.option('--ssh_server', type=str, help="server to ssh login", required=False)
@click.option('--server_port', type=int, help="server port", required=False)
@click.option('--remote_host', type=str, help="remote host for port forwarding", required=False)
@click.option('--login_user', type=str, help="login user of ssh server", required=False)
@click.argument('ssh_argument', required=False)
def add(ctx, name, forward_type, local_port, host_port, ssh_server, server_port, remote_host, login_user, ssh_argument):
    try:
        AddCommand(ctx).run()
    except RuntimeError as error:
        raise ClickException(error)


@main.command(help='list existing port forwarding targets')
@click.pass_context
def list(ctx):
    ListCommand(ctx).run()


@main.command(help='delete specified target')
@click.option('-n', '--name', type=str, help="name of port fowarding")
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    DeleteCommand(ctx).run()


@main.command(help='generate ssh port forward parameters')
@click.argument('name')
@click.pass_context
def param(ctx, name):
    ParameterCommand(ctx).run()


if __name__ == '__main__':
    main()
