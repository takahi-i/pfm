# -*- coding: utf-8 -*-

"""Console script for pfm."""

import click

from pf_manager.pfm_command.delete import DeleteCommand
from pf_manager.pfm_command.list import ListCommand


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
def add(ctx):
    print("called add")
    pass


@main.command(help='list existing targets')
@click.pass_context
def list(ctx):
    ListCommand(ctx).run()


@main.command(help='delete specified target')
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    DeleteCommand(ctx).run()
    pass


@main.command(help='generate ssh port forward parameters')
@click.argument('name')
@click.pass_context
def parameter(ctx):
    print("called parameter")
    pass


if __name__ == '__main__':
    main()
