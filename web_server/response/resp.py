from functools import wraps
from flask import Response
from flask import request
import json

def add_headers(func):
    @wraps(func)
    def add(*args, **kwargs):
        result = func(*args, **kwargs)
        resp = Response(result)

        headers = request.headers
        orgin = headers.get('Origin')
        if orgin:
            resp.headers['Access-Control-Allow-Origin'] = orgin

        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'

        return resp
    return add


def success_response(data=None):
    resp_dict = {}
    resp_dict['code'] = 0
    resp_dict['msg'] = 'success'
    resp_dict['data'] = data

    return json.dumps(resp_dict)


def failed_response(code,msg):
    resp_dict = {}
    resp_dict['code'] = code
    resp_dict['msg'] = msg

    return json.dumps(resp_dict)
