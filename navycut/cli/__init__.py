import click
from ._exec_cli import _create_boiler_project

@click.group()
def _execute_from_command_line():
    """execute navycut commands from command line."""
    pass

@_execute_from_command_line.command()
@click.argument('name')
def createproject(name):
    """Create the navycut project at the specified directory."""
    _create_boiler_project(name)