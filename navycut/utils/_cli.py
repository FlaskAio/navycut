from ..errors.misc import InsufficientArgumentsError
from . import input
from .logger import Console
from ._exec_cli import (_show_help, 
                _create_boiler_project)

_cli_dict = {
    "help": ["_show_help", "To show all the available commands."],
    "--help" : ["_show_help", "To show all the available commands."],
    "createproject" : ["_create_boiler_project", "To start a new project."],
    "create_project" : ["_create_boiler_project", "To start a new project."],
    "create-project" : ["_create_boiler_project", "To start a new project."],
}

def _execute_from_command_line(argv):
    if len(argv) < 2: raise InsufficientArgumentsError("add --help or help for more details.")
    if argv[1].lower() in list(_cli_dict.keys()):
        globals()[_cli_dict[argv[1].lower()][0]](_cli_dict, argv)
    else: 
        Console.log.Error(f"{argv[1].lower()} invalid option selected. Please type `help` for details.")
