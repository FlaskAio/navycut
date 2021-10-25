from .cli import print_version
import click


@click.command()
@click.option('-V', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def _main():
    from .cli import _execute_from_command_line
    return _execute_from_command_line()

if __name__ == '__main__':
    _main()