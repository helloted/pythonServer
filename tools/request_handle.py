#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
请求的处理的一些公用方法
"""
from functools import wraps
from flask import request
from log_util.app_logger import logger
import json
from response import failed_resp,success_resp
from response.errors import *
from redis_manager import redis_center,redis_web_center
from functools import wraps
from flask import Response
from flask import request
import json
from werkzeug.datastructures import MultiDict
import traceback
from flask import session


from functools import wraps
from flask import Response
from flask import request
from flask import session as webSession
import json
from werkzeug.datastructures import MultiDict
import traceback


def web_transfer(func):
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
                    body = json.loads(body)
                except Exception:
                    logger.error(traceback.format_exc())
                    logger.info('WEB -> HF: {method} {route} {post_str}'.format(method=request.method, route=route,post_str=body))
            if body:
                logger.info('WEB -> HF: {method} {route} {body}'.format(method=request.method, route=route,body=json.dumps(body)))
            else:
                body = {}
            result = func(body, *args, **kwargs)
        elif request.method == 'OPTIONS':
            result = success_resp().data
        else:
            logger.info('WEB -> HF: {method} {route}'.format(method=request.method, route=route))
            result = func(*args, **kwargs)

        if not isinstance(result,Response):
            resp = Response(result)
        else:
            resp = result
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

def request_unpack(func):
    @wraps(func)
    def unpack(*args, **kwargs):
        route = request.url[21:]
        method = request.method
        if method == 'GET':
            logger.info('APP -> HF: {method} {route}'.format(method=request.method, route=route))
            result = func(*args, **kwargs)
        else:
            body = request.json
            if not body:
                body = request.form
            logger.info('APP -> HF: {method} {route} {body}'.format(method=request.method, route=route,body=json.dumps(body)))
            result = func(body,*args, **kwargs)
        return result
    return unpack


def login_required(func):
    @wraps(func)
    def token_verfiy(*args, **kwargs):
        # phone = request.args.get('phone')
        # token = request.args.get('token')
        #
        # redis_token = redis_center.get(phone)
        #
        # if not token:
        #     res= failed_resp(ERROR_Login_First)
        #     logger.info(res.log)
        #     return res.data
        #
        # if token != redis_token:
        #     resp= failed_resp(ERROR_Token_Invalid)
        #     logger.info(resp.log)
        #     return resp.data

        result = func(*args, **kwargs)
        return result
    return token_verfiy



def web_login_required(func):
    @wraps(func)
    def token_verfiy(*args, **kwargs):
        if 'login_status' not in webSession or webSession['login_status'] != 'login':
            resp= failed_resp(ERROR_Login_First)
            logger.info(resp.log)
            return resp.data
        result = func(*args, **kwargs)
        return result
    return token_verfiy


def manager_authorization_required(func):
    @wraps(func)
    def manager_authorization(*args, **kwargs):
        if 'agent_id' not in webSession or webSession['agent_id'] != 1:
            resp= failed_resp(ERROR_Authorization)
            logger.info(resp.log)
            return resp.data
        result = func(*args, **kwargs)
        return result
    return manager_authorization
