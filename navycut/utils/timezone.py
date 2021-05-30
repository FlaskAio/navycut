from datetime import (
            datetime as datetime_,
            date as date_,
            )
import pytz
import time

class datetime(datetime_):

    def __init__(self, *wargs, **kwargs):
        super(datetime, self).__init__(*wargs, **kwargs)

class TimeZone:
    
    @classmethod
    def today(cls):
        return datetime.now()