from flask import current_app
from flask_script import Manager
from flask_migrate import MigrateCommand
from webbrowser import open_new_tab
from threading import Timer
from ..utils._exec_cli import _create_boiler_app
from ..utils.security import create_password_hash
from ..utils.console import Console
from ..core import app
from ..orm.sqla import sql
from os import path
from alembic import command
from ..conf import get_settings_module
from ..orm.sqla.migrator import (
            Config as MigratorConfig, 
            _perform_migration
            )

class Command:
    def __init__(self):
        app._attach_settings_modules()
        self.manager = Manager(app)
        self._playAll()

    def _playAll(self):
        self.manager.add_command('db',MigrateCommand)
        @self.manager.command
        def drop_db():
            if Console.input.Boolean( "Are you sure, you want to lose all your data"):
                with app.app_context(): 
                    try:
                        sql.drop_all()
                        Console.log.Success("models dropped successfully.") 
                    except Exception:
                        Console.log.Error("Unable to drop the database. \nSomething went Wrong with database conf.")
            else: Console.log.Error("Service canceled")
        
        @self.manager.command
        def runserver(port=None):
            port = port or 8888
            host =  '127.0.0.1'
            # res = self._open_web_browser(f"http://{host}:{port}")
            # Timer(1, open_new_tab(f"http://{host}:{port}") ).start()
            
            app.run_wsgi(port=port, host=host)
            # open_new_tab(f"http://{host}:{port}")

        @self.manager.command
        def migrate():
            """Creates a new migration repository"""
            directory = current_app.extensions['migrate'].directory
            if not path.exists(directory):
                config = MigratorConfig()
                config.set_main_option('script_location', directory)
                config.config_file_name = path.join(directory, 'alembic.ini')
                config = current_app.extensions['migrate'].\
                    migrate.call_configure_callbacks(config)
                command.init(config, directory, 'flask')
                _perform_migration()
            else: _perform_migration()

        
        @self.manager.command
        def makemigrations():
            from ..admin.site.models import _insert_intial_data
            _insert_intial_data()
            return None
        
        @self.manager.command
        def createsuperuser():
            from ..admin.site.models import User, Group
            
            name:str = Console.input.String("enter admin name: ")
            email:str = Console.input.String("enter admin email: ")
            username:str = Console.input.String("enter admin username: ") or email
            while True:
                password:str = Console.input.String("enter admin password: ")
                confirm_password:str = Console.input.String("enter admin confirm password: ")
                if not password == confirm_password:
                    Console.log.Warning('confirm password not matched.\nPlease enter again.')
                    continue
                else: break
            if Console.input.Boolean( "Are you sure, you want to create superuser using inserted data"):
                with app.app_context():
                    new_admin = User(first_name=name.rsplit(" ")[0], last_name=name.rsplit(" ")[1], email=email, 
                            username=username, password=create_password_hash(password))
                    group = Group.query.filter_by(name='super_admin').first()
                    new_admin.groups.append(group)
                    new_admin.save()
                    Console.log.Success("superuser created successfully.")
            else: Console.log.Error("superuser creation canceled!")
        @self.manager.command
        def createapp(app_name):
            settings = get_settings_module()
            project_dir = settings.BASE_DIR
            _create_boiler_app(app_name, project_dir)

    def run(self):
        self.manager.run()
    
    def add_command(self, name, command):
        self.manager.add_command(name, command)