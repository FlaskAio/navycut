from sys import argv
# from .errors.misc import InsufficientArgumentsError
from .utils._cli import _execute_from_command_line


# def main() -> None:
#     if len(argv) < 2: raise InsufficientArgumentsError()

def _main():
    return _execute_from_command_line(argv)

if __name__ == '__main__':
    _main()