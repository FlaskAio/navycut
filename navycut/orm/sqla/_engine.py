import typing as t

def MYSQL_ENGINE(creds:t.Dict[str, str]) -> str:
    return 'mysql+pymysql://{0}:{1}@{2}/{3}'\
                .format(creds['username'],
                        creds['password'],
                        creds['host'],
                        creds['database'])

def SQLITE_ENGINE(creds:t.Dict[str, str]) -> str:
    return f'sqlite:///{creds.get("database")}'

def POSTRESQL_ENGINE(creds:t.Dict[str, str]) -> str:
    return f"postgresql://\
        {creds.get('username')}:{creds.get('password')}@\
            {creds.get('host')}/{creds.get('database')}"