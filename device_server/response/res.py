
from device_server.response.errors import DeviceServerError
import json
import struct
import collections

SERVER = 'HF'

class Send():
    def __init__(self,data,log):
        self.data = data
        self.log = log


def head_pack(data):
    headPack = struct.pack("!1I", data.__len__())
    send = headPack+data
    return send


def response(device_sn,orgin_data,content):
    content['code'] = 0
    content['msg'] = 'success'
    orgin_data['content'] = content
    jsonrsp = json.dumps(orgin_data)

    send_data = head_pack(jsonrsp)

    log = SERVER + ' -> ' + device_sn + ', ' + jsonrsp
    send = Send(send_data,log)

    return send


def fail_response(device_sn,orgin_data,error):
    content = collections.OrderedDict()
    content['code'] = error.code
    content['msg'] = error.msg

    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)

    send_data = head_pack(jsonrsp)
    log = SERVER + ' -> ' + device_sn + ', ' + jsonrsp
    send = Send(send_data,log)

    return send


def fail_response_with_str(device_sn,orgin_data,error_str):
    content = collections.OrderedDict()
    content['code'] = 1
    content['msg'] = error_str
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)

    send_data = head_pack(jsonrsp)
    log = SERVER + ' -> ' + device_sn + ', ' + jsonrsp
    send = Send(send_data,log)

    return send


def fail_response_content(device_sn,orgin_data,error,content):
    content['code'] = error.code
    content['msg'] = error.msg
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)

    send_data = head_pack(jsonrsp)
    log = SERVER + ' -> ' + device_sn + ', ' + jsonrsp
    send = Send(send_data,log)

    return send


def success_response(device_sn,orgin_data):
    content = {}
    content['code'] = 0
    content['msg'] = 'success'
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)

    send_data = head_pack(jsonrsp)
    log = SERVER + ' -> ' + device_sn + ', ' + jsonrsp
    send = Send(send_data,log)

    return send


def succss_response_content(device_sn,orgin_data,content):
    content['code'] = 0
    content['msg'] = 'success'
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)

    send_data = head_pack(jsonrsp)
    log = SERVER + ' -> ' + device_sn + ', ' + jsonrsp
    send = Send(send_data,log)

    return send


def push_data(device_sn,cmd,seq,content):
    data = {}
    data['content'] = content
    data['version'] = 1
    data['seq'] = seq
    data['cmd'] = cmd

    jsonrsp = json.dumps(data)

    send_data = head_pack(jsonrsp)
    log = SERVER + ' -> ' + device_sn + ', ' + jsonrsp
    send = Send(send_data,log)

    return send

