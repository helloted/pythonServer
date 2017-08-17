#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.15
主动往打印机推送
"""

import collections
import json
from redis_manager import redis_center,r_queue
from log_util.device_logger import logger
from gevent._socket2 import _closedsocket
import sockets_controller
from device_server.response.res import success_response,fail_response,fail_response_content,head_pack
from device_server.response import errors
from device_server.db_tool import SessionContext
from super_models.device_model import Device
import time, gevent
from redis_manager import r_upload_token
import hashlib


keep_socket = None

def print_response(data):
    global keep_socket
    send = success_response(data)
    logger.info('received print content success')
    keep_socket.send(send)


def heart_beat(data,tcp_socket):
    send = success_response(data)
    try:
        tcp_socket.send(send)
    except Exception,e:
        logger.error(e.message)


def print_request(data,web_socket):
    global keep_socket
    keep_socket = web_socket

    web_content = data.get('content')

    device_sn = web_content.get('device_sn')
    post_time = web_content.get('post_time')
    print_content = web_content.get('content')
    device_socket = sockets_controller.get_socket(device_sn)

    if device_socket:
        logger.info('get the tcp_socket:' + device_sn)

        dic = collections.OrderedDict()
        dic['cmd'] = 'print_content'
        dic['version'] = '1.0'
        dic['seq'] = 4

        content = collections.OrderedDict()
        content['device_sn'] = device_sn
        content['post_time'] = post_time
        content['content_sn'] = device_sn
        content['print_content'] = print_content

        dic['content'] = content

        jsresp = json.dumps(dic)
        try:
            device_socket.send(head_pack(jsresp))
        except Exception, e:
            logger.info('the tcpsocket can,t send')
            sockets_controller.pop_socket(device_sn)
            fail_data = {}
            fail_data['device_sn'] = device_sn
            fail_data['post_time'] = post_time
            send = fail_response(data,errors.ERROR_Device_Offline)
            keep_socket.send(send)
    else:
        logger.info('device %s is not connecting', device_sn)
        content = {}
        content['device_sn'] = device_sn
        content['post_time'] = post_time
        send = fail_response(data,errors.ERROR_Device_Offline)
        keep_socket.send(send)


def update_setting(data,web_socket):
    global keep_socket
    keep_socket = web_socket

    web_content = data.get('content')

    device_sn = str(web_content)

    # device_sn = web_content.get('device_sn')
    # post_time = web_content.get('post_time')
    # print_content = web_content.get('content')
    device_socket = sockets_controller.get_socket(device_sn)

    if device_socket:
        logger.info('get the tcp_socket:' + device_sn)

        dic = collections.OrderedDict()
        dic['cmd'] = 'update_setting'
        dic['version'] = '1.0'
        dic['seq'] = 10

        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=device_sn).first()

            content = collections.OrderedDict()
            content['newest_setting_version'] = device.newest_setting_version
            content['wifi_name'] = device.wifi_name
            content['wifi_password'] = device.wifi_password
            content['wifi_encrypt_type'] = device.wifi_encrypt_type
            content['capture_baudrate'] = device.capture_baudrate
            content['app_print_baudrate'] = device.app_print_baudrate
            content['app_received_baudrate'] = device.app_received_baudrate
            content['net_port'] = device.net_port
            content['ip_white_list'] = None
            content['bluetooth_white_list'] = None

            if device.ip_white_list:
                content['ip_white_list'] = json.loads(device.ip_white_list)

            if device.bluetooth_white_list:
                content['bluetooth_white_list'] = json.loads(device.bluetooth_white_list)


        dic['content'] = content

        logger.info(('update_setting',dic))

        jsresp = json.dumps(dic)
        try:
            device_socket.send(head_pack(jsresp))
        except Exception, e:
            logger.info('the tcpsocket can,t send')
            sockets_controller.pop_socket(device_sn)
            content = {}
            content['device_sn'] = device_sn
            send = fail_response_content(data,errors.ERROR_Device_Offline,content)
            keep_socket.send(send)
    else:
        logger.info('device %s is not connecting', device_sn)
        content = {}
        content['device_sn'] = device_sn
        send = fail_response_content(data, errors.ERROR_Device_Offline, content)
        keep_socket.send(send)


def update_app(data,web_socket):
    global keep_socket
    keep_socket = web_socket

    web_content = data.get('content')

    device_sn = web_content.get('device_sn')
    newest_url = web_content.get('newest_url')
    device_socket = sockets_controller.get_socket(device_sn)

    if device_socket:
        logger.info('get the tcp_socket:' + device_sn)

        dic = collections.OrderedDict()
        dic['cmd'] = 'update_app'
        dic['version'] = '1.0'
        dic['seq'] = 10

        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=device_sn).first()

            content = collections.OrderedDict()
            content['newest_url'] = newest_url


        dic['content'] = content

        jsresp = json.dumps(dic)
        try:
            device_socket.send(head_pack(jsresp))
            logger.info(jsresp)
        except Exception, e:
            logger.info('the tcpsocket can,t send')
            sockets_controller.pop_socket(device_sn)
            rsp_content = {}
            rsp_content['device_sn'] = device_sn
            send = fail_response_content(data, errors.ERROR_Device_Offline, rsp_content)
            keep_socket.send(send)
    else:
        logger.info('device %s is not connecting', device_sn)
        rsp_content = {}
        rsp_content['device_sn'] = device_sn
        send = fail_response_content(data, errors.ERROR_Device_Offline, rsp_content)
        keep_socket.send(send)


def update_token(task):
    device_sn = task.get('device_sn')
    key = 'anthoer'
    key_id = 1
    device_socket = sockets_controller.get_socket(device_sn)
    if device_socket:
        logger.info('get the tcp_socket:' + device_sn)

        dic = collections.OrderedDict()
        dic['cmd'] = 'update_token'
        dic['version'] = '1.0'
        dic['seq'] = 10

        content = {}
        content['key_id'] = key_id
        content['key'] = key

        dic['content'] = content

        jsresp = json.dumps(dic)
        try:
            device_socket.send(head_pack(jsresp))
            logger.info(jsresp)
        except Exception, e:
            logger.info('the tcpsocket can,t send')
            sockets_controller.pop_socket(device_sn)
            return False
        else:
            return True
    else:
        logger.info('canot find the device')
        return False


def receive_push_queue():
    while True:
        task_package = r_queue.brpop('devices_queue', 0)
        task_str = task_package[1]
        task_dict = eval(task_str)
        task_type = task_dict['type']
        if task_type == 'update_token':
            update_token(task_dict)
            logger.info(task_dict)
        gevent.sleep(0)


def received_update_token(data,tcp_socket):
    content = data.get('content')
    if type(content) == type(''):
        content = eval(content)
    key = content.get('key')
    store_token = hashlib.md5(tcp_socket.device_sn + key).hexdigest()
    r_upload_token.set(tcp_socket.device_sn, store_token)

