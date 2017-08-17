#coding=utf-8

"""
caohaozhi@swindtech.com
2017.07.03
给APP端的响应
"""

from app_server.response.errors import *
import json
from log_util.app_logger import logger
from flask import request


def dberror_handle(exe_val):
    logger.error(exe_val)
    # print 'dberror handele'
    # resp_dict = {}
    # resp_dict['code'] = 102
    # resp_dict['msg'] = str(exe_val)
    #
    # resp_json = json.dumps(resp_dict)
    #
    #
    #
    # return resp_json


def success_resp(data=None):
    resp_dict = {}
    resp_dict['code'] = 0
    resp_dict['msg'] = 'success'
    resp_dict['data'] = data
    resp_json = json.dumps(resp_dict)
    orgin = request.headers.get('Origin')
    response_headers = {}
    if orgin:
        response_headers['Access-Control-Allow-Origin'] = orgin
    response_headers['Content-Type'] = 'text/json'
    response_headers['Access-Control-Allow-Credentials'] = 'true'
    response_headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS"
    response_headers["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept"
    return resp_json,response_headers


def failed_resp(error):
    logger.info(error.msg)
    resp_dict = {}
    resp_dict['code'] = error.code
    resp_dict['msg'] = error.msg

    resp_json = json.dumps(resp_dict)

    orgin = request.headers.get('Origin')
    response_headers = {}
    if orgin:
        response_headers['Access-Control-Allow-Origin'] = orgin
    response_headers['Content-Type'] = 'text/json'
    response_headers['Access-Control-Allow-Credentials'] = 'true'

    return resp_json,response_headers

def failed_resp_full(code=None, msg=None):
    resp_dict = {}
    resp_dict['code'] = code
    resp_dict['msg'] = msg

    resp_json = json.dumps(resp_dict)

    orgin = request.headers.get('Origin')
    response_headers = {}
    if orgin:
        response_headers['Access-Control-Allow-Origin'] = orgin
    response_headers['Content-Type'] = 'text/json'
    response_headers['Access-Control-Allow-Credentials'] = 'true'

    return resp_json,response_headers