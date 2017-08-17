
from device_server.response.errors import DeviceServerError
import json
import struct
import collections

def head_pack(data):
    headPack = struct.pack("!1I", data.__len__())
    send = headPack+data
    return send



def response(orgin_data,content):
    content['code'] = 0
    content['msg'] = 'success'
    orgin_data['content'] = content
    jsonrsp = json.dumps(orgin_data)
    send = head_pack(jsonrsp)
    return send


def fail_response(orgin_data,error):
    content = collections.OrderedDict()
    content['code'] = error.code
    content['msg'] = error.msg
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)
    send = head_pack(jsonrsp)

    return send


def fail_response_with_str(orgin_data,error_str):
    content = collections.OrderedDict()
    content['code'] = 1
    content['msg'] = error_str
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)
    send = head_pack(jsonrsp)

    return send


def fail_response_content(orgin_data,error,content):
    content['code'] = error.code
    content['msg'] = error.msg
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)
    send = head_pack(jsonrsp)

    return send


def success_response(orgin_data):
    content = {}
    content['code'] = 0
    content['msg'] = 'success'
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)
    send = head_pack(jsonrsp)

    return send


def succss_response_content(orgin_data,content):
    content['code'] = 0
    content['msg'] = 'success'
    orgin_data['content'] = content

    jsonrsp = json.dumps(orgin_data)
    send = head_pack(jsonrsp)

    return send