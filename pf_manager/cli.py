# -*- coding: utf-8 -*-

"""Console script for pfm."""

import click

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
    ctx.obj['config'] = ctx.params["config"]


@main.command(help='add port forwarding target')
@click.pass_context
@click.option('-n', '--name', type=str, help="name of port fowarding")
@click.argument('ssh_param')
def add(ctx, name, ssh_param):
    AddCommand(ctx).run()

@main.command(help='list existing targets')
@click.pass_context
def list(ctx):
    ListCommand(ctx).run()


@main.command(help='delete specified target')
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
