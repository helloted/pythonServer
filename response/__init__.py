#coding=utf-8

"""
caohaozhi@swindtech.com
2017.07.03
给APP端的响应
"""

from response.errors import *
import json
from log_util.app_logger import logger
from flask import request

class Response():
    def __init__(self,data,log):
        self.data = data
        self.log = log

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
    data = json.dumps(resp_dict)

    log = 'HF -> Client: {resp}'.format(resp=data)

    resp = Response(data,log)

    return resp


def failed_resp(error):
    resp_dict = {}
    resp_dict['code'] = error.code
    resp_dict['msg'] = error.msg
    data = json.dumps(resp_dict)
    log = 'HF -> Client: {resp}'.format(resp=data)
    resp = Response(data, log)
    return resp
