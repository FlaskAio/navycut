from navycut.core import app, models
# from navycut.core.app_config import Navycut
from flask import Blueprint, render_template, Flask

# app = Flask(__name__)

# rest_api = Blueprint('rest_api', __name__)
# # bp = Blueprint(name="bp", import_name=__name__)

from flask import Response
from flask.json import dumps

def JsonResponse(data=None, **kwargs) -> Response: return Response(dumps(data), mimetype='application/json') if data is not None else Response(dumps(kwargs), mimetype='application/json')


from ab import bp
app.register_blueprint(bp)
# app.register_blueprint(rest_api)

# @bp.route("/")
# def index():
#     return render_template('index.html')

@app.route("/aniket")
def aniket():
    return JsonResponse([1,2])

if __name__ == "__main__":app.run(debug=True)