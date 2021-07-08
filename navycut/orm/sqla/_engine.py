def MYSQL_ENGINE(creds=dict()):
    return 'mysql+pymysql://{0}:{1}@{2}/{3}'\
                .format(creds['username'],
                        creds['password'],
                        creds['host'],
                        creds['database'])

def SQLITE_ENGINE(creds=dict()):
    return f'sqlite:///{creds.get("database")}'