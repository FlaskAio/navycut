from .sqla._engine import (MYSQL_ENGINE, 
                    SQLITE_ENGINE)
import typing

avaliable_engine:typing.DefaultDict = dict(
            mysql = "MYSQL_ENGINE",
            sqlite = "SQLITE_ENGINE",
            sqlite3 = "SQLITE_ENGINE"
            )


def _generate_engine_uri(db_details:dict = None) -> typing.AnyStr:
    if db_details is not None: 
        engine_type:typing.AnyStr = db_details.get('engine')
        if engine_type in list(avaliable_engine.keys()):
            return globals()[avaliable_engine.get(engine_type)](db_details.get('creds'))
