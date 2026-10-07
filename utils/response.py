from flask import jsonify
import json
from flask import current_app
# from utils.util import CustomJSONEncoder

def success_response(data, message, http_code=200):
    body = {
        "data": data,
        "message": message,
        "status": False
    }

    return jsonify(body), http_code


def error_response(message, http_code=400, data=None):
    body = {
        "data": data,
        "message": message,
        "status": False
    }

    return jsonify(body), http_code
