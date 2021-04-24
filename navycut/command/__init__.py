from flask_script import prompt_bool, Manager
from flask_migrate import Migrate, MigrateCommand
from ..admin.model import BaseUser
from werkzeug.security import generate_password_hash

class Command:
    def __init__(self, app=None, models=None):
        self.app = app
        self.models = models
        if app and models is not None:
            self.manager = Manager(app)
            Migrate(self.app, self.models)
            self._playAll()

    def init(self, app, models):
        self.app = app
        self.models  = models
        self.manager = Manager(app)
        Migrate(self.app, self.models)
        self._playAll()

    def _playAll(self):
        self.manager.add_command('models', MigrateCommand)
        self.manager.add_command('db',MigrateCommand)
        @self.manager.command
        def drop_models():
            if prompt_bool( "Are you sure you want to lose all your data"):
                with self.app.app_context(): self.models.drop_all()
                print ("[+] models dropped successfully.") 
            else: print("[!] Service canceled")
        @self.manager.command
        def runserver(port=None, host=None, debug=None):
            port = port or 8888
            host = host or '0.0.0.0'
            debug = debug or 'False'
            self.app.run(port=port, host=host, debug=debug)
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
                with self.app.app_context():
                    newAdmin = BaseUser(name=name, email=email, username=username, 
                                        password=generate_password_hash(password))
                    self.models.session.add(newAdmin)
                    self.models.session.commit()
                    print("superuser created successfully")
            else: print("superuser creation canceled!")

    def run(self):
        self.manager.run()
    
    def add_command(self, name, command):
        self.manager.add_command(name, command)

command = Command()