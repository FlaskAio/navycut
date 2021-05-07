from os import path
from pathlib import Path
from flask_script import prompt_bool, Manager
from flask_migrate import Migrate, MigrateCommand
from ..admin.site.models import User, Group, _insert_intial_data
from ..utils._exec_cli import _create_boiler_app
from ..utils.security import create_password_hash
from ..core import app
from ..orm.db import db

class Command:
    def __init__(self):
        self.manager = Manager(app)
        Migrate(app, db)
        self._playAll()

    # def init(self, settings):
    #     self.settings = settings
    #     self.manager = Manager(app)
    #     Migrate(app, db)
    #     self._playAll()

    def _playAll(self):
        self.manager.add_command('db',MigrateCommand)
        @self.manager.command
        def drop_db():
            if prompt_bool( "Are you sure you want to lose all your data"):
                with app.app_context(): db.drop_all()
                print ("[+] models dropped successfully.") 
            else: print("[!] Service canceled")
        
        @self.manager.command
        def runserver(port=None, host=None):
            port = port or 8888
            host = host or '127.0.0.1'
            # debug =  app.debug or False
            app.run(port=port, host=host, debug=app.debug)
        
        @self.manager.command
        def makemigrations():
            _insert_intial_data()
            pass
        
        @self.manager.command
        def createsuperuser():
            name:str = input("enter admin name: ")
            email:str = input("enter admin email: ")
            username:str = input("enter admin username: ") or email
            while True:
                password:str = input("enter admin password: ")
                confirm_password:str = input("enter admin confirm password:")
                if not password == confirm_password:
                    print('confirm password not matched.')
                    continue
                else: break
            if prompt_bool( "Are you sure to create superuser using inserted data"):
                with app.app_context():
                    new_admin = User(first_name=name.rsplit(" ")[0], last_name=name.rsplit(" ")[1], email=email, 
                            username=username, password=create_password_hash(password))
                    group = Group.query.filter_by(name='super_admin').first()
                    new_admin.groups.append(group)
                    new_admin.save()
                    print("superuser created successfully")
            else: print("superuser creation canceled!")
        @self.manager.command
        def createapp(app_name):
            project_dir = Path(path.abspath(app.config.get('BASE_DIR')))
            _create_boiler_app(app_name, project_dir)

    def run(self):
        self.manager.run()
    
    def add_command(self, name, command):
        self.manager.add_command(name, command)




_Command = Command()