from flask import Flask, jsonify
import logging
from logging.config import dictConfig
from a2wsgi import WSGIMiddleware

# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(message="Hello world!")

# app.wsgi_app = WhiteNoise(app.wsgi_app, root='/static')
app.debug=True
application = WSGIMiddleware(app)


# if __name__ == "__main__":
    # app.run()
    # serve(TransLogger(app, setup_console_handler=False), listen='*:8000')
    # serve(app, listen='*:8000')