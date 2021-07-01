import click
from ._exec_cli import _create_boiler_project
from navycut import get_version

@click.group()
@click.option("--version", 
        callback=get_version,
        help="Get the Navycut version.")
        
def _execute_from_command_line():
    """execute navycut commands from command line."""
    pass

@click.command()
@click.argument('name')
def createproject(name):
    """Create the navycut project at the specified directory."""
    _create_boiler_project(name)

@click.command()
def version():
    print (get_version())


_execute_from_command_line.add_command(createproject)
_execute_from_command_line.add_command(version)