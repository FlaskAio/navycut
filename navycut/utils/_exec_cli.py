from os import mkdir, path, listdir
from pathlib import Path
from sys import argv
from .logger import Console
from .tools import generate_random_secret_key
from ..errors.misc import InsufficientArgumentsError, DirectoryAlreadyExistsError

__baseDir__ = Path(path.abspath(__file__)).parent.parent


def _show_help(_cli_dict, *wargs) -> None:
    Console.log.Info("--------------------------------------------------")
    for key, value in _cli_dict.items():
        Console.log.Info(f"{key} ----- {value[1]}")
    Console.log.Info("--------------------------------------------------")

def _write_file():
    pass

def _create_boiler_project(*wargs):
    if len(argv) < 2: 
        Console.log.Error("A valid project is required.")
        raise InsufficientArgumentsError("Provide a valid project name")
    project_name = argv[2].lower()
    if path.exists(project_name): 
        Console.log.Error(f"A project already exists with the same name: {project_name}. Try some another name.")
        raise DirectoryAlreadyExistsError(project_name)
    mkdir(project_name)
    project_dir = Path(path.realpath(project_name))
    boilerplate_dir = __baseDir__ / 'boiler_create_project'
    Console.log.Info(f"Empty project folder created.\nProject name: {project_name}\nLocation: {str(project_dir)}")
    #start reading exiting boiler plate
    Console.log.Info('Started writing the default boiler files for project')
    boilerplate_dir__files = listdir(boilerplate_dir)
    boilerplate_dir__files.remove("__pycache__") if "__pycache__" in boilerplate_dir__files else None
    for boiler_file in boilerplate_dir__files:
        if path.isdir(boilerplate_dir / boiler_file) and boiler_file == "project_dir___boiler_dir":
            mkdir(project_dir / project_name)
            for bff in listdir(boilerplate_dir / boiler_file):
                if bff == '__pycache__': continue
                with open(boilerplate_dir / boiler_file / bff, 'r') as bfffb:
                    with open(project_dir / project_name / bff, 'w') as bffwb:
                        if bff == 'settings.py':
                            settings_data = bfffb.read()
                            #now replace the __secretkey__ with the real one at the new project directory.
                            settings_data=settings_data.replace("__secretkey_____boiler_var", generate_random_secret_key(53))
                            bffwb.write(settings_data)
                        else: bffwb.write(bfffb.read())
                Console.log.Info(f'data from {boilerplate_dir / boiler_file / bff} successfully transfered to {project_dir / project_name / bff}')
        else:
            with open(boilerplate_dir / boiler_file, 'r') as fb:
                with open(project_dir / boiler_file, 'w') as wb:
                    if boiler_file == 'manage.py':
                        manage_data = fb.read()
                        #now replace the __secretkey__ with the real one at the new project directory.
                        manage_data=manage_data.replace("project_name___boiler_var", project_name)
                        wb.write(manage_data)
                    else: wb.write(fb.read())
                Console.log.Info(f'Data from {boilerplate_dir / boiler_file} successfully transferred to {project_dir}/{boiler_file}')
    Console.log.Success(f"project {project_name} created successfully.")

def _create_boiler_app(app_name, project_dir, *wargs):
    app_dir = project_dir / app_name
    if path.exists(app_dir): 
        Console.log.Error(f"A app already exists with the same name: {app_name} at {project_dir}. Try some another name.")
        raise DirectoryAlreadyExistsError(app_dir)
    mkdir (app_dir)
    Console.log.Info(f"Empty app folder named {app_name} created.\nProject name: {app_name}\nLocation: {str(app_dir)}")
    boilerplate_dir = __baseDir__ / 'boiler_create_app'
    Console.log.Info('Started writing the default boiler files for app')
    boilerplate_dir__files = listdir(boilerplate_dir)
    boilerplate_dir__files.remove("__pycache__") if "__pycache__" in boilerplate_dir__files else None
    for boiler_file in boilerplate_dir__files:
        if path.isdir(boilerplate_dir / boiler_file):
            with open(boilerplate_dir / boiler_file / "README.md", 'r') as tmr:
                mkdir(app_dir / boiler_file)
                Console.log.Info(f"Empty directory created at: {app_dir/boiler_file}")
                with open(app_dir / boiler_file / "README.md", 'w') as tmw:
                    tmw.write(tmr.read())
            Console.log.Info(f'Data from {boilerplate_dir}/{boiler_file}/README.md successfully transferred to {app_dir}/{boiler_file}/README.md')
        else:
            with open(boilerplate_dir / boiler_file, 'r') as fb:
                with open(app_dir / boiler_file, 'w') as wb:
                    if boiler_file == '__init__.py':
                        settings_data = fb.read()
                        #now replace the import_name with the real one at the new project directory.
                        settings_data=settings_data.replace("import_name___boiler_var", app_name)
                        wb.write(settings_data)
                    else: wb.write(fb.read())
                Console.log.Info(f'Data from {boilerplate_dir}/{boiler_file} successfully transferred to {app_dir}/{boiler_file}')
    Console.log.Success(f"app {app_name} created successfully.")