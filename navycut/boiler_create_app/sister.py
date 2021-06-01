"""
Do not change anything if you dont have enough knowledge 
how to handle it, otherwise it may mess the server.
"""

from navycut.core import SisterApp
from os.path import abspath
from pathlib import Path
from .urls import url_patterns

__basedir__ = Path(abspath(__file__)).parent


app = SisterApp(name="import_name___boiler_var",
                import_name= __name__,
                template_folder=__basedir__ / "templates",
                static_folder=__basedir__ / "static",
                static_url_path="/static",
                url_prefix="/import_name___boiler_var",)

app.add_url_pattern(url_patterns)
app.import_app_features()