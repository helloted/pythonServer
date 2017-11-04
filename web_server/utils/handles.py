from functools import wraps
from flask import Response
from flask import request
import json
from log_util.web_demo_logger import logger
from werkzeug.datastructures import MultiDict
from web_server.utils.response import response_success
import traceback


def transfer(func):
    @wraps(func)
    def handle(*args, **kwargs):
        route = request.url[21:]

        if request.method == 'POST':
            body = request.form
            if body and isinstance(body,MultiDict):
                body = body.to_dict()

            if not body:
                body = request.data

            if body and isinstance(body, str):
                try:
                    body = eval(body)
                except Exception:
                    logger.error(traceback.format_exc())
                    logger.info('Client -> HF: {method} {route} {post_str}'.format(method=request.method, route=route,post_str=body))
            if body:
                logger.info('Client -> HF: {method} {route} {body}'.format(method=request.method, route=route,body=json.dumps(body)))
            else:
                body = {}
            result = func(body, *args, **kwargs)
        elif request.method == 'OPTIONS':
            result = response_success().resp_data
        else:
            logger.info('Client -> HF: {method} {route}'.format(method=request.method, route=route))
            result = func(*args, **kwargs)

        resp = Response(result)
        headers = request.headers
        orgin = headers.get('Origin')
        if orgin:
            resp.headers['Access-Control-Allow-Origin'] = orgin

        resp.headers['Content-Type'] = 'application/json; charset=UTF-8'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        resp.headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept"
        return resp

    return handle