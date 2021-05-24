import click
from ._exec_cli import _create_boiler_project

@click.group()
def _execute_from_command_line():
    """execute navycut commands from command line."""
    pass

@click.command()
@click.argument('name')
def createproject(name):
    _create_boiler_project(name)

_execute_from_command_line.add_command(createproject)