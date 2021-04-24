from navycut.core import app, models
# from navycut.core.app_config import Navycut
from flask import Blueprint, render_template, Flask

# app = Flask(__name__)

# rest_api = Blueprint('rest_api', __name__)
# # bp = Blueprint(name="bp", import_name=__name__)
from ab import bp
app.register_blueprint(bp)
# app.register_blueprint(rest_api)

# @bp.route("/")
# def index():
#     return render_template('index.html')

@app.route("/aniket")
def aniket():
    return render_template('admin/login.html')

if __name__ == "__main__":app.run(debug=True)