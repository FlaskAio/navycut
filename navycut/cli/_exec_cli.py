from os import makedirs, listdir
from ..utils import path
from nc_console import Console
from ..utils.tools import (generate_random_secret_key, 
                    snake_to_camel_case
                    )
from ..errors.misc import  DirectoryAlreadyExistsError

__baseDir__ = path.abspath(__file__).parent.parent


def _create_boiler_project(name):
    project_name = name

    if path.exists(project_name): 
        Console.log.Error(f"A project already exists with the same name: {project_name}. Try some another name.")
        raise DirectoryAlreadyExistsError(project_name)
    
    makedirs(project_name)
    project_dir = path.realpath(project_name)
    boilerplate_dir = __baseDir__ / 'boiler_create_project'
    Console.log.Info(f"Empty project folder created.\nProject name: {project_name}\nLocation: {str(project_dir)}")
    #start reading the existing boiler plate
    Console.log.Info('Started writing the default boiler files for project')
    boilerplate_dir__files = listdir(boilerplate_dir)
    boilerplate_dir__files.remove("__pycache__") if "__pycache__" in boilerplate_dir__files else None
    
    for boiler_file in boilerplate_dir__files:
        
        if path.isDir(boilerplate_dir / boiler_file) and boiler_file == "project_dir___boiler_dir":
            makedirs(project_dir / project_name)
            
            for bff in listdir(boilerplate_dir / boiler_file):
                
                if bff == '__pycache__': continue
                with open(boilerplate_dir / boiler_file / bff, 'r') as bfffb:
                    
                    with open(project_dir / project_name / bff, 'w') as bffwb:
                        if bff == 'settings.py':
                            settings_data = bfffb.read()
                            #now replace the __secretkey__ with the real one at the new project directory.
                            settings_data=settings_data.replace("__secretkey_____boiler_var", generate_random_secret_key(53)).replace("project_name___boiler_var", project_name)
                            bffwb.write(settings_data)
                        
                        elif bff == 'wsgi.py' or bff == "asgi.py":
                            wsgi_data = bfffb.read()
                            wsgi_data = wsgi_data.replace("project_name___boiler_var", project_name)
                            bffwb.write(wsgi_data)
                        
                        else: 
                            bffwb.write(bfffb.read())
                
                Console.log.Info(f'data from {boilerplate_dir / boiler_file / bff} successfully transfered to {project_dir / project_name / bff}')
        
        elif path.isDir(boilerplate_dir / boiler_file) and boiler_file == 'templates':
            
            with open(boilerplate_dir / boiler_file / "README.md", 'r') as tmr:
                makedirs(project_dir / boiler_file)
                Console.log.Info(f"Empty template directory created at: {project_dir/boiler_file}")
               
                with open(project_dir / boiler_file / "README.md", 'w') as tmw:
                    tmw.write(tmr.read())
                Console.log.Info(f"Data from README.md successfully transferred to {project_dir/boiler_file/'README.md'}")

        else:
            with open(boilerplate_dir / boiler_file, 'r') as fb:
                
                with open(project_dir / boiler_file, 'w') as wb:
                    
                    if boiler_file == 'manage.py':
                        manage_data = fb.read()
                        #now replace the __secretkey__ with the real one at the new project directory.
                        manage_data=manage_data.replace("project_name___boiler_var", project_name)
                        wb.write(manage_data)
                    
                    else: 
                        wb.write(fb.read())
                Console.log.Info(f'Data from {boilerplate_dir / boiler_file} successfully transferred to {project_dir}/{boiler_file}')
    Console.log.Success(f"project {project_name} created successfully.")

def _create_boiler_app(app_name, project_dir, *wargs):
    app_dir = project_dir / app_name
    
    if path.exists(app_dir): 
        Console.log.Error(f"A app already exists with the same name: {app_name} at {project_dir}. Try some another name.")
        raise DirectoryAlreadyExistsError(app_dir)
    
    makedirs (app_dir)
    Console.log.Info(f"Empty app folder named {app_name} created.\App name: {app_name}\nLocation: {str(app_dir)}")
    boilerplate_dir = __baseDir__ / 'boiler_create_app'
    Console.log.Info('Started writing the default boiler files for app')
    boilerplate_dir__files = listdir(boilerplate_dir)
    boilerplate_dir__files.remove("__pycache__") if "__pycache__" in boilerplate_dir__files else None
    
    for boiler_file in boilerplate_dir__files:
        with open(boilerplate_dir / boiler_file, 'r') as fb:
            
            with open(app_dir / boiler_file, 'w') as wb:
               
                if boiler_file == 'sister.py':
                    sister_data = fb.read()
                    #now replace the import_name with the real one at the new project directory.
                    sister_data=sister_data.replace("import_name___boiler_var", app_name)
                    sister_data=sister_data.replace("classname___boiler_var", f"{snake_to_camel_case(app_name)}Sister")
                    wb.write(sister_data)
                
                else: 
                    wb.write(fb.read())
            Console.log.Info(f'Data from {boilerplate_dir}/{boiler_file} successfully transferred to {app_dir}/{boiler_file}')
    Console.log.Success(f"app {app_name} created successfully.")