# -*- coding: utf-8 -*-

"""Console script for pfm."""

import click
import os

from pf_manager.pf_command.add import AddCommand
from pf_manager.pf_command.delete import DeleteCommand
from pf_manager.pf_command.list import ListCommand
from pf_manager.pf_command.param import ParameterCommand
from pf_manager.pf_command.update import UpdateCommand
from pf_manager.pf_command.connect import ConnectCommand
from pf_manager.util.log import logger

PFM_VERSION = '0.5.0'


def print_version(ctx):
    click.echo('Version ' + PFM_VERSION)
    ctx.exit()


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


@main.command(help='Add port forward setting')
@click.pass_context
@click.option('-n', '--name', type=str, help="Name of port fowarding", required=False)
@click.option('--forward-type', type=str, help="Port forwarding type [L or R]", required=False, default='L')
@click.option('--local-port', type=int, help="Local port", required=False)
@click.option('--remote-port', type=int, help="Port of remote host", required=False)
@click.option('--ssh-server', type=str, help="Server to ssh login", required=False)
@click.option('--server-port', type=int, help="Server port", required=False)
@click.option('--remote-host', type=str, help="Remote host for port forwarding", required=False, default='localhost')
@click.option('--login-user', type=str, help="Login user of ssh server", required=False)
@click.argument('ssh-argument', required=False)
def add(ctx, name, forward_type, local_port, remote_port, ssh_server, server_port, remote_host, login_user,
        ssh_argument):
    try:
        AddCommand(name, ssh_argument, forward_type, remote_host, remote_port, local_port, ssh_server, server_port,
                   login_user, ctx.obj["config"]).run()
    except RuntimeError as error:
        logger.warn("Failed to register...")
        logger.warn(error)


@main.command(help='Update registered port forward setting')
@click.pass_context
@click.option('-n', '--name', type=str, help="Name of port fowarding", required=False)
@click.option('--forward-type', type=str, help="Port forwarding type [L or R]", required=False, default='L')
@click.option('--local-port', type=int, help="Local port", required=False)
@click.option('--remote-port', type=int, help="Port of remote host", required=False)
@click.option('--ssh-server', type=str, help="Server to ssh login", required=False)
@click.option('--server-port', type=int, help="Server port", required=False)
@click.option('--remote-host', type=str, help="Remote host for port forwarding", required=False, default='localhost')
@click.option('--login-user', type=str, help="Login user of ssh server", required=False)
def update(ctx, name, forward_type, local_port, remote_port, ssh_server, server_port, remote_host, login_user):
    try:
        UpdateCommand(name, forward_type, remote_host, remote_port, local_port, ssh_server, server_port,
                      login_user, ctx.obj["config"]).run()
    except RuntimeError as error:
        logger.warn("Failed to register...")
        logger.warn(error)


@main.command(help='List existing port forward settings')
@click.pass_context
def list(ctx):
    ListCommand(ctx.obj["config"]).run()


@main.command(help='Delete specified setting')
@click.option('-n', '--name', type=str, help="name of port fowarding")
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    DeleteCommand(ctx.obj["config"], name).run()


@main.command(help='Generate ssh port forward parameters')
@click.argument('name')
@click.pass_context
def param(ctx, name):
    ParameterCommand(ctx.obj["config"], name).run()


@main.command(help='SSH connection with a specified setting')
@click.argument('name')
@click.pass_context
def connect(ctx, name):
    ConnectCommand(ctx.obj["config"], name).run()


@main.command(help='Show version number')
@click.pass_context
def version(ctx):
    print_version(ctx)


if __name__ == '__main__':
    main()
