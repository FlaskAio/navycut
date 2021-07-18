# # from .sqla._engine import (MYSQL_ENGINE, 
# #                     SQLITE_ENGINE,
# #                     POSTRESQL_ENGINE)
# import typing as t

# # avaliable_engine:t.DefaultDict = {
# #             "sqla.mysql" : "MYSQL_ENGINE",
# #             "sqla.sqlite" : "SQLITE_ENGINE",
# #             "sqla.sqlite3" : "SQLITE_ENGINE",
# #             "sqla.postgresql" : "POSTRESQL_ENGINE"
# #             }




# def _generate_engine_uri(db_details:dict = None) -> t.AnyStr:
#     if db_details is not None: 
#         engine_type:t.AnyStr = db_details.get('engine')
#         if engine_type in list(avaliable_engine.keys()):
#             return globals()[avaliable_engine.get(engine_type)](db_details.get('creds'))
