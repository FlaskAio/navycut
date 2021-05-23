from flask import Flask, jsonify
import requests as r

app = Flask(__name__)

async def get(url):
    return r.get(url)

@app.route("/")
async def index():
    data = await get("https://api.github.com/repos/django/django")
    data = data.json()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
















# from navycut.datastructures import NCObject
# from json import dumps

# a={
#    "name": "Partha Das",
#    "age" : "26",
#    "address" : {
#        "city" : "kolkata",
#        "area" : {
#            "country" : {"IN" : "India"},
#        }
#    }
# }

# nc = NCObject(a)



# # nc.update({"name":"Aniket Sarkar"})
# nc.address.area.country.update(UK="England")
# print (nc.address.area.country.UK)


# nc.na me






# from logging import debug
# from flask import Flask, jsonify
# from a2wsgi import WSGIMiddleware
# from uvicorn import run
# import uvicorn

# # dictConfig({
# #     'version': 1,
# #     'formatters': {'default': {
# #         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
# #     }},
# #     'handlers': {'wsgi': {
# #         'class': 'logging.StreamHandler',
# #         'stream': 'ext://flask.logging.wsgi_errors_stream',
# #         'formatter': 'default'
# #     }},
# #     'root': {
# #         'level': 'INFO',
# #         'handlers': ['wsgi']
# #     }
# # })

# app = Flask(__name__)

# @app.route("/")
# async def index():
#     return jsonify(message="Hello world!")

# # app.wsgi_app = WhiteNoise(app.wsgi_app, root='/static')
# app.debug=True
# application = WSGIMiddleware(app)




# if __name__ == "__main__":
#     uvicorn.run(application, port=9500, debug=True)
#     # serve(TransLogger(app, setup_console_handler=False), listen='*:8000')
#     # serve(app, listen='*:8000')