import typing as t

if t.TYPE_CHECKING:
    from navycut.core.app_config import Navycut

"""
the default engine setup for all type 
of databases available for SQLAlchemy.
"""

def _database_url_setter(app:t.Type["Navycut"], uri:str) -> True:
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    return True

def mysql(app:t.Type["Navycut"], 
            creds:t.Dict[str, str]
            ) -> None:
    
    database_uri = f"mysql+pymysql://{creds['username']}:\
        {creds['password']}@{creds['host']}/{creds['database']}"
    
    _database_url_setter(app, database_uri)

def sqlite(app:t.Type["Navycut"], 
            creds:t.Dict[str, str]
            ) -> None:
    
    database_uri = f'sqlite:///{creds.get("database")}'
    
    _database_url_setter(app, database_uri)

def sqlite3(app:t.Type["Navycut"], 
            creds:t.Dict[str, str]
            ) -> None:
    return sqlite(app, creds)

def postgresql(app:t.Type["Navycut"], 
            creds:t.Dict[str, str]
            ) -> None:
    database_uri = f"postgresql://\
        {creds.get('username')}:{creds.get('password')}@\
            {creds.get('host')}/{creds.get('database')}"

    _database_url_setter(app, database_uri)