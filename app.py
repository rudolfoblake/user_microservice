import json
import requests
import base64
from flask import Flask, request
from Controllers import routeController
rc = routeController.RouteControl()
from Controllers import inputController
ic = inputController.InputControl()

app = Flask(__name__)

@app.route("/user/auth/register", methods=['POST'])
def register_route():
    transfrom_to_dict = ic.json_to_dict(request)
    if transfrom_to_dict[1] != 200:
        return transfrom_to_dict
    result = rc.register_route(transfrom_to_dict[0])
    return result


@app.route("/user/<string:id>")
def get_user_by_id_route(id):
    result = rc.get_user_by_id_route(id)
    return result


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5030)