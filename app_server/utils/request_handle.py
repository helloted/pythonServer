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
from redis_manager import redis_center
from app_server.response import failed_resp
from app_server.response.errors import *


def basic_unpack(func):
    @wraps(func)
    def unpack(*args, **kwargs):
        url = request.url
        method = request.method
        if method == 'GET':
            logger.info(('GET',url))
        else:
            body = request.json
            if not body:
                body = request.form
            logger.info((url,body))
        result = func(*args, **kwargs)
        return result
    return unpack


def login_required(func):
    @wraps(func)
    def token_verfiy(*args, **kwargs):
        user_id = request.args.get('user_id')
        token = request.args.get('token')

        key = 'app_user_token' + str(user_id)
        redis_token = redis_center.get(key)

        if not token:
            return failed_resp(ERROR_Login_First)

        if token != redis_token:
            return failed_resp(ERROR_Token_Invalid)

        result = func(*args, **kwargs)
        return result
    return token_verfiy