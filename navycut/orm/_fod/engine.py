def _MYSQL_ENGINE(creds=dict()):
    return 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(creds['username'],creds['password'],creds['host'],creds['database'])

def _SQLITE_ENGINE(name='navycut.sqlite3'):
    return 'sqlite:///{0}'.format(name)