import click
from os import path
from alembic import command
from ..cli._exec_cli import _create_boiler_app
from ..utils.security import create_password_hash
from ..utils.console import Console
from ..core import app
from ..conf import get_settings_module
from ..orm.sqla.migrator import (
            Config as MigratorConfig, 
            _perform_migration,
            _perform_makemigrations
            )


@click.group()
def manage_command():
    """manage the command executed using manage.py"""
    app._attach_settings_modules()

@manage_command.command()
@click.argument('addrport', default="127.0.0.1:8888")
def runserver(addrport):
    
    """Starts a lightweight and interactive Web server for development."""

    if addrport is not None: 
        port = int(addrport.split(":")[1])
        host = str(addrport.split(":")[0])
    app.run_wsgi(port=port, host=host)

@manage_command.command()
@click.option('-d', '--directory', default=None,
              help=('Migration script directory (default is "migrations")'))
@click.option('-m', '--message', default=None, help='Revision message')
@click.option('--sql', is_flag=True,
              help=('Don\'t emit SQL to database - dump to standard output '
                    'instead'))
@click.option('--head', default='head',
              help=('Specify head revision or <branchname>@head to base new '
                    'revision on'))
@click.option('--splice', is_flag=True,
              help=('Allow a non-head revision as the "head" to splice onto'))
@click.option('--branch-label', default=None,
              help=('Specify a branch label to apply to the new revision'))
@click.option('--version-path', default=None,
              help=('Specify specific path from config for version file'))
@click.option('--rev-id', default=None,
              help=('Specify a hardcoded revision id instead of generating '
                    'one'))
@click.option('-x', '--x-arg', multiple=True,
              help='Additional arguments consumed by custom env.py scripts')
def migrate(directory, message, sql, head, splice, branch_label, version_path,
            rev_id, x_arg):
    
    """Updates database schema. Manages both apps with migrations and those without."""
    
    directory = app.extensions['migrate'].directory
    
    if not path.exists(directory):
        config = MigratorConfig()
        config.set_main_option('script_location', directory)
        config.config_file_name = path.join(directory, 'alembic.ini')
        config = app.extensions['migrate']\
            .migrate.call_configure_callbacks(config)
        command.init(config, directory, 'flask')
        with app.app_context():
            _perform_migration(directory, message, sql, head, splice, branch_label, version_path,
                            rev_id, x_arg)
    
    else: 
        with app.app_context():
            _perform_migration(directory, message, sql, head, splice, branch_label, version_path,
                        rev_id, x_arg)

@manage_command.command()
@click.option('-d', '--directory', default=None,
              help=('Migration script directory (default is "migrations")'))
@click.option('--sql', is_flag=True,
              help=('Don\'t emit SQL to database - dump to standard output '
                    'instead'))
@click.option('--tag', default=None,
              help=('Arbitrary "tag" name - can be used by custom env.py '
                    'scripts'))
@click.option('-x', '--x-arg', multiple=True,
              help='Additional arguments consumed by custom env.py scripts')
@click.argument('revision', default='head')
def makemigrations(directory, sql, tag, x_arg, revision):
    """Creates new migration(s) for apps."""
    from ..admin.site.models import _insert_intial_data
    with app.app_context():
        _perform_makemigrations(directory, revision, sql, tag, x_arg)
        try: 
            _insert_intial_data()
        except:
            pass
    return None

@manage_command.command()
@click.option('-n', '--name', default=None,
              help=('Provide the name of superuser (default is None)'))

@click.option('-u', '--username', default=None,
              help=('Provide the username of superuser (default is None)'))

@click.option('-e', '--email', default=None,
              help=('Provide the email of superuser (default is None)'))

def createsuperuser(name, username, email):
    
    """Create the superuser account to access the admin panel."""
    
    from ..admin.site.models import User, Group
            
    name:str = name or Console.input.String("enter admin name: ")
    email:str = email or Console.input.String("enter admin email: ")
    username:str = username or Console.input.String("enter admin username: ") or email
    while True:
        password:str = Console.input.Password("enter admin password: ")
        confirm_password:str = Console.input.Password("enter admin confirm password: ")
        if not password == confirm_password:
            Console.log.Warning('confirm password not matched.\nPlease enter again.')
            continue
        else: 
            break
    
    if Console.input.Boolean( "Are you sure, you want to create superuser using inserted data"):
        with app.app_context():
            new_admin = User(first_name=name.rsplit(" ")[0], last_name=name.rsplit(" ")[1], email=email, 
                    username=username, password=password)
            group = Group.query.filter_by(name='super_admin').first()
            new_admin.groups.append(group)
            new_admin.save()
            Console.log.Success("superuser created successfully.")
    else: 
        Console.log.Error("superuser creation canceled!")

@manage_command.command()
@click.argument("name")
def createapp(name):
    """Creates a Navycut app directory structure for the given app name in the current directory."""
    settings = get_settings_module()
    project_dir = settings.BASE_DIR
    _create_boiler_app(name, project_dir)