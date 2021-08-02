import click
import sys
from os import environ
from ..utils import path
import typing as t
from operator import attrgetter
from alembic import command
from flask.globals import current_app
from ..cli._exec_cli import _create_boiler_app
from ..utils.tools import get_default_username
from nc_console import Console
from ..core import app
from ..contrib.decorators import with_appcontext
from ..conf import settings
from ..orm.sqla.migrator import (
            Config as MigratorConfig, 
            _perform_migrate,
            _perform_makemigrations
            )

if t.TYPE_CHECKING:
    from ..core import Navycut

@click.group()
def manage_command():
    """manage the command executed using manage.py"""
    app._attach_settings_modules()

@manage_command.command("runserver")
@click.argument('addrport', default="127.0.0.1:8888")
def runserver(addrport):
    
    """Starts a lightweight and interactive Web server for development."""

    if addrport is not None: 
        port = int(addrport.split(":")[1])
        host = str(addrport.split(":")[0])
    app.run_wsgi(port=port, host=host)

@manage_command.command("makemigrations")
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
def makemigrations(directory, message, sql, head, splice, branch_label, version_path,
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
            _perform_makemigrations(directory, message, sql, head, splice, branch_label, version_path,
                            rev_id, x_arg)
    
    else: 
        with app.app_context():
            _perform_makemigrations(directory, message, sql, head, splice, branch_label, version_path,
                        rev_id, x_arg)

@manage_command.command("migrate")
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
def migrate(directory, sql, tag, x_arg, revision):
    """Creates new migration(s) for apps."""
    from ..contrib.auth.models import _insert_intial_data
    with app.app_context():
        _perform_migrate(directory, revision, sql, tag, x_arg)
        try: 
            _insert_intial_data()
        except:
            pass
    return None

@manage_command.command("sqlmigrate")
@click.argument('revision', default='head')
def sql_migrate(revision):
    """
    Prints the SQL statements for the named migration.
    """
    with app.app_context():
        _perform_migrate(revision=revision, sql=True)


@manage_command.command("createsuperuser")
@click.option('-n', '--name', default=None,
              help=('Provide the name of superuser (default is None)'))

@click.option('-u', '--username', default=None,
              help=('Provide the username of superuser (default is None)'))

@click.option('-e', '--email', default=None,
              help=('Provide the email of superuser (default is None)'))

def createsuperuser(name, username, email):
    
    """Create the superuser account to access the admin panel."""
    
    from ..contrib.auth.models import User, Group
            
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

@manage_command.command("changepassword")
@click.argument("username", default=get_default_username())
@with_appcontext
def change_password(username):
    """
    Change a user's password for django.contrib.admin.
    """
    from ..contrib.auth.models import _get_user_by_username

    user = _get_user_by_username(username)
    if user is None:
        Console.log.Error(f"user '{username}' does not exists.")
    else:
        while True:
            passwd1 = Console.input.Password("Enter password: ")
            passwd2 = Console.input.Password("Enter password again: ")
            if not passwd1 == passwd2:
                Console.log.Warning("password not matched.\nTry again.")
                continue
            else:
                user.set_password(passwd1)
                Console.log.Success(f"Password changed successfully for user '{username}'")
                break


@manage_command.command("createapp")
@click.argument("name")
def createapp(name):
    """Creates a Navycut app directory structure for the given app name in the current directory."""
    project_dir = settings.BASE_DIR
    _create_boiler_app(name, project_dir)

@manage_command.command("shell", short_help="Run a shell in the app context.")
@with_appcontext
def shell():
    """
    Run an interactive Python shell in the context of a given
    navycut application.  The application will populate the default
    namespace of this shell according to its configuration.

    This is useful for executing small snippets of management code
    without having to manually configure the application.
    """
    import code
    from flask.globals import _app_ctx_stack

    _app:t.Type["Navycut"] = _app_ctx_stack.top.app
    banner = (
        f"Python {sys.version} on {sys.platform}\n"
        f"Project: {_app.config.get('PROJECT_NAME')} \n"
        f"Debug mode: {'on' if _app.debug else 'off'}\n"
        f"Instance: {_app.instance_path}\n"
        "(InteractiveConsole)"
    )
    ctx: dict = dict()

    # Support the regular Python interpreter startup script if someone
    # is using it.
    startup = environ.get("PYTHONSTARTUP")
    if startup and path.isfile(startup):
        with open(startup) as f:
            eval(compile(f.read(), startup, "exec"), ctx)

    ctx.update(app.make_shell_context())

    # Site, customize, or startup script can set a hook to call when
    # entering interactive mode. The default one sets up readline with
    # tab and history completion.
    interactive_hook = getattr(sys, "__interactivehook__", None)
    

    if interactive_hook is not None:
        try:
            import readline
            from rlcompleter import Completer
        except ImportError:
            pass
        else:
            # rlcompleter uses __main__.__dict__ by default, which is
            # flask.__main__. Use the shell context instead.
            readline.set_completer(Completer(ctx).complete)

        interactive_hook()

    code.interact(banner=banner, local=ctx)

@manage_command.command("routes", short_help="Show the routes for the app.")
@click.option(
    "--sort",
    "-s",
    type=click.Choice(("endpoint", "methods", "rule", "match")),
    default="endpoint",
    help=(
        'Method to sort routes by. "match" is the order that Flask will match '
        "routes when dispatching a request."
    ),
)
@click.option("--all-methods", is_flag=True, help="Show HEAD and OPTIONS methods.")
@with_appcontext
def routes_command(sort: str, all_methods: bool) -> None:
    """Show all registered routes with endpoints and methods."""

    rules = list(current_app.url_map.iter_rules())
    if not rules:
        click.echo("No routes were registered.")
        return

    ignored_methods = set(() if all_methods else ("HEAD", "OPTIONS"))

    if sort in ("endpoint", "rule"):
        rules = sorted(rules, key=attrgetter(sort))
    elif sort == "methods":
        rules = sorted(rules, key=lambda rule: sorted(rule.methods))  # type: ignore

    rule_methods = [
        ", ".join(sorted(rule.methods - ignored_methods))  # type: ignore
        for rule in rules
    ]

    headers = ("Endpoint", "Methods", "Rule")
    widths = (
        max(len(rule.endpoint) for rule in rules),
        max(len(methods) for methods in rule_methods),
        max(len(rule.rule) for rule in rules),
    )
    widths = [max(len(h), w) for h, w in zip(headers, widths)]
    row = "{{0:<{0}}}  {{1:<{1}}}  {{2:<{2}}}".format(*widths)

    click.echo(row.format(*headers).strip())
    click.echo(row.format(*("-" * width for width in widths)))

    for rule, methods in zip(rules, rule_methods):
        click.echo(row.format(rule.endpoint, methods, rule.rule).rstrip())