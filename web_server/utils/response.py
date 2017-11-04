import json


class ResponseData():
    def __init__(self,resp_data,log):
        self.resp_data = resp_data
        self.log = log


def response_success(data=None):
    resp_dict = {}
    resp_dict['code'] = 0
    resp_dict['msg'] = 'success'
    resp_dict['data'] = data

    resp_json = json.dumps(resp_dict)

    log = 'HF -> Client: {resp}'.format(resp=resp_json)
    resp = ResponseData(resp_json,log)

    return resp


def response_failed(error):
    resp_dict = {}
    resp_dict['code'] = error.code
    resp_dict['msg'] = error.msg

    resp_json = json.dumps(resp_dict)

    log = 'HF -> Client: {resp}'.format(resp=resp_json)
    resp = ResponseData(resp_json,log)

    return resp
