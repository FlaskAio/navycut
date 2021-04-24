from flask import Blueprint, render_template
from os.path import abspath
from pathlib import Path

_basedir = Path(abspath(__file__)).parent

bp = Blueprint(name="bp", import_name=__name__, template_folder=_basedir/'aniket_temp')


@bp.route("/index")
def index():
    return render_template('ind.html')