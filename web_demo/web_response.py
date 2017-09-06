import json
from log_util.web_demo_logger import logger


def success_resp(data=None):
    resp_dict = {}
    resp_dict['code'] = 0
    resp_dict['msg'] = 'success'
    resp_dict['data'] = data
    resp_json = json.dumps(resp_dict)
    return resp_json


def failed_resp(error):
    logger.info(error.msg)
    resp_dict = {}
    resp_dict['code'] = error.code
    resp_dict['msg'] = error.msg

    resp_json = json.dumps(resp_dict)

    return resp_json

def failed_resp_full(code=None, msg=None):
    resp_dict = {}
    resp_dict['code'] = code
    resp_dict['msg'] = msg

    resp_json = json.dumps(resp_dict)

    return resp_json