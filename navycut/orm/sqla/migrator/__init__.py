from flask_migrate import Migrate as _Migrate
from os import path
from flask import current_app
from alembic import command
from alembic.config import Config as AlembicConfig
from argparse import Namespace

class Config(AlembicConfig):
    def get_template_directory(self):
        template_dir = path.join(path.abspath(path.dirname(__file__)), "templates")
        print ("template_dir:", template_dir)
        return template_dir

class Migrate(_Migrate):
    def __init__(self, *wargs, **kwargs):
        super(Migrate, self).__init__(*wargs, **kwargs)

    # def init_app(self, app, db, directory, **kwargs):
    #     return super().init_app(app, db=db, directory=directory, **kwargs)

    def get_config(self, directory=None, x_arg=None, opts=None):
        if directory is None:
            directory = str(self.directory)
        config = Config(path.join(directory, 'alembic.ini'))
        config.set_main_option('script_location', directory)
        if config.cmd_opts is None:
            config.cmd_opts = Namespace()
        for opt in opts or []:
            setattr(config.cmd_opts, opt, True)
        if not hasattr(config.cmd_opts, 'x'):
            if x_arg is not None:
                setattr(config.cmd_opts, 'x', [])
                if isinstance(x_arg, list) or isinstance(x_arg, tuple):
                    for x in x_arg:
                        config.cmd_opts.x.append(x)
                else:
                    config.cmd_opts.x.append(x_arg)
            else:
                setattr(config.cmd_opts, 'x', None)
        return self.call_configure_callbacks(config)


def _perform_makemigrations(directory=None, message=None, sql=False, head='head', splice=False,
            branch_label=None, version_path=None, rev_id=None, x_arg=None):
    """Alias for 'revision --autogenerate'"""
    config = current_app.extensions['migrate'].migrate.get_config(
        directory, opts=['autogenerate'], x_arg=x_arg)
    command.revision(config, message, autogenerate=True, sql=sql,
                     head=head, splice=splice, branch_label=branch_label,
                     version_path=version_path, rev_id=rev_id)

def _perform_migrate(directory=None, revision='head', sql=False, tag=None, x_arg=None):
    
    config = current_app.extensions['migrate'].migrate.get_config(directory,
                                                                  x_arg=x_arg)
    command.upgrade(config, revision, sql=sql, tag=tag)


migrate:Migrate=Migrate()