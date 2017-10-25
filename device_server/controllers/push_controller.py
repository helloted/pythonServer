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
from device_server.response.res import success_response,fail_response,fail_response_content,head_pack,push_data
from device_server.response import errors
from device_server.db_tool import SessionContext
from super_models.device_model import Device
import time, gevent
from redis_manager import r_upload_token,redis_web_device
import hashlib


keep_socket = None

def print_response(data,tcp_socket):
    device_sn = tcp_socket.device_sn
    post_time = data.get('post_time')
    to_web_channel = device_sn + str(post_time)
    redis_center.publish(to_web_channel, data)
    logger.info('{device}  print content success,now return to web'.format(device=device_sn))

#
#
# def heart_beat(data,tcp_socket):
#     send = success_response(data)
#     try:
#         tcp_socket.send(send.data)
#     except Exception, e:
#         logger.error(e)
#     else:
#         logger.info(send.log)
#
#
# def print_request(data,web_socket):
#     global keep_socket
#     keep_socket = web_socket
#
#     web_content = data.get('content')
#
#     device_sn = web_content.get('device_sn')
#     post_time = web_content.get('post_time')
#     print_content = web_content.get('content')
#     device_socket = sockets_controller.get_socket(device_sn)
#
#     if device_socket:
#         logger.info('get the tcp_socket:' + device_sn)
#
#         dic = collections.OrderedDict()
#         dic['cmd'] = 'print_content'
#         dic['version'] = '1.0'
#         dic['seq'] = 4
#
#         content = collections.OrderedDict()
#         content['device_sn'] = device_sn
#         content['post_time'] = post_time
#         content['content_sn'] = device_sn
#         content['print_content'] = print_content
#
#         dic['content'] = content
#
#         jsresp = json.dumps(dic)
#         try:
#             device_socket.send(head_pack(jsresp))
#         except Exception, e:
#             logger.info('the tcpsocket can,t send')
#             sockets_controller.pop_socket(device_sn)
#             fail_data = {}
#             fail_data['device_sn'] = device_sn
#             fail_data['post_time'] = post_time
#             send = fail_response(data,errors.ERROR_Device_Offline)
#             try:
#                 keep_socket.send(send.data)
#             except Exception, e:
#                 logger.error(e)
#             else:
#                 logger.info(send.log)
#     else:
#         logger.info('cannot find the device:{device} to push print content'.format(device=device_sn))
#         content = {}
#         content['device_sn'] = device_sn
#         content['post_time'] = post_time
#         send = fail_response(data,errors.ERROR_Device_Offline)
#         try:
#             keep_socket.send(send.data)
#         except Exception, e:
#             logger.error(e)
#         else:
#             logger.info(send.log)
#
#
# def update_setting(data,web_socket):
#     global keep_socket
#     keep_socket = web_socket
#
#     web_content = data.get('content')
#
#     device_sn = str(web_content)
#
#     # device_sn = web_content.get('device_sn')
#     # post_time = web_content.get('post_time')
#     # print_content = web_content.get('content')
#     device_socket = sockets_controller.get_socket(device_sn)
#
#     if device_socket:
#         logger.info('get the tcp_socket:' + device_sn)
#
#         content = collections.OrderedDict()
#         with SessionContext() as session:
#             device = session.query(Device).filter_by(sn=device_sn).first()
#
#             content['newest_setting_version'] = device.newest_setting_version
#             content['wifi_name'] = device.wifi_name
#             content['wifi_password'] = device.wifi_password
#             content['wifi_encrypt_type'] = device.wifi_encrypt_type
#             content['capture_baudrate'] = device.capture_baudrate
#             content['app_print_baudrate'] = device.app_print_baudrate
#             content['app_received_baudrate'] = device.app_received_baudrate
#             content['net_port'] = device.net_port
#             content['ip_white_list'] = None
#             content['bluetooth_white_list'] = None
#             content['justification'] = device.justification
#             content['add_qr'] = device.add_qr
#
#             if device.ip_white_list:
#                 content['ip_white_list'] = json.loads(device.ip_white_list)
#
#             if device.bluetooth_white_list:
#                 content['bluetooth_white_list'] = json.loads(device.bluetooth_white_list)
#
#             if device.order_invalid_keys:
#                 content['order_invalid_keys'] = json.loads(device.order_invalid_keys)
#
#             if device.order_valid_keys:
#                 content['order_valid_keys'] = json.loads(device.order_valid_keys)
#
#             if device.cut_cmds:
#                 content['cut_cmds'] = json.loads(device.cut_cmds)
#
#
#         send = push_data(device_sn,'update_setting',10,content)
#         try:
#             device_socket.send(send.data)
#         except Exception, e:
#             logger.info('the tcpsocket can,t send')
#             sockets_controller.pop_socket(device_sn)
#             content = {}
#             content['device_sn'] = device_sn
#             web_send = fail_response_content(data,errors.ERROR_Device_Offline,content)
#             try:
#                 keep_socket.send(web_send.data)
#             except Exception, e:
#                 logger.error(e)
#             else:
#                 logger.info(web_send.log)
#         else:
#             logger.info(send.log)
#     else:
#         logger.info('cannot find the device:{device} to update setting'.format(device=device_sn))
#         content = {}
#         content['device_sn'] = device_sn
#         send = fail_response_content(data, errors.ERROR_Device_Offline, content)
#         try:
#             keep_socket.send(send.data)
#         except Exception, e:
#             logger.error(e)
#         else:
#             logger.info(send.log)


# def update_app(data,web_socket):
#     global keep_socket
#     keep_socket = web_socket
#
#     web_content = data.get('content')
#
#     device_sn = web_content.get('device_sn')
#     newest_url = web_content.get('newest_url')
#     device_socket = sockets_controller.get_socket(device_sn)
#
#     if device_socket:
#         logger.info('ready to update app, get the tcp_socket:' + device_sn)
#         content = collections.OrderedDict()
#         content['newest_url'] = newest_url
#         update_send = push_data(device_sn,'update_app',12,content)
#         try:
#             device_socket.send(update_send.data)
#         except Exception, e:
#             logger.info('the tcpsocket can,t send')
#             sockets_controller.pop_socket(device_sn)
#             rsp_content = {}
#             rsp_content['device_sn'] = device_sn
#             send = fail_response_content(data, errors.ERROR_Device_Offline, rsp_content)
#             try:
#                 keep_socket.send(send.data)
#             except Exception, e:
#                 logger.error(e)
#             else:
#                 logger.info(send.log)
#         else:
#             logger.info(update_send.log)
#     else:
#         logger.info('cannot find the device:{device} to update app'.format(device=device_sn))
#         rsp_content = {}
#         rsp_content['device_sn'] = device_sn
#         send = fail_response_content(data, errors.ERROR_Device_Offline, rsp_content)
#         try:
#             keep_socket.send(send.data)
#         except Exception,e:
#             logger.error(e)
#         else:
#             logger.info(send.log)


def update_token(task):
    device_sn = task.get('device_sn')
    key = 'anthoer'
    key_id = 1
    device_socket = sockets_controller.get_socket(device_sn)
    if device_socket:
        logger.info('get the tcp_socket:{device}, ready to update token'.format(device=device_sn))
        content = {}
        content['key_id'] = key_id
        content['key'] = key
        token_data = push_data(device_sn,'update_token',14,content)
        try:
            device_socket.send(token_data.data)
        except Exception, e:
            logger.error(e)
            sockets_controller.pop_socket(device_sn)
            return False
        else:
            logger.info(token_data.log)
            return True
    else:
        logger.info('cannot find the device:{device} to update token'.format(device=device_sn))
        return False

def upload_log(task):
    device_sn = task.get('device_sn')
    time = task.get('time')

    device_socket = sockets_controller.get_socket(device_sn)
    if device_socket:
        logger.info('get the tcp_socket:{device}, ready to upload log'.format(device=device_sn))
        content = {}
        content['time'] = time

        send = push_data(device_sn,'upload_log',16,content)
        try:
            device_socket.send(send.data)
        except Exception, e:
            logger.error(e)
            sockets_controller.pop_socket(device_sn)
            return False
        else:
            logger.info(send.log)
            return True
    else:
        logger.info('cannot find the device:{device} to upload log'.format(device=device_sn))
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

        if task_type == 'kill_socket':
            device_sn = task_dict['device_sn']
            sockets_controller.kill_socket(device_sn)

        if task_type == 'upload_log':
            upload_log(task_dict)
            logger.info(task_dict)
        gevent.sleep(0)


def cloud_print(web_data):
    device_sn = web_data.get('device_sn')
    post_time = web_data.get('post_time')
    print_content = web_data.get('content')
    device_socket = sockets_controller.get_socket(device_sn)

    content = {}
    content['device_sn'] = device_sn
    content['post_time'] = post_time

    to_web_channel = device_sn + str(post_time)

    to_web_faild = {'code':1,'msg':'failed'}

    if not device_socket:
        logger.info('cannot find the device:{device} to push print content'.format(device=device_sn))
        redis_center.publish(to_web_channel, to_web_faild)
    else:
        logger.info('get the tcp_socket:' + device_sn)
        content = collections.OrderedDict()
        content['device_sn'] = device_sn
        content['post_time'] = post_time
        content['content_sn'] = device_sn
        content['print_content'] = print_content

        send = push_data(device_sn,'print_content', 4, content)

        logger.info(send)

        try:
            device_socket.send(send.data)
        except Exception, e:
            logger.error(e)
            logger.info('can not send cloud print to {device}'.format(device=device_sn))
            sockets_controller.pop_socket(device_sn)
            redis_center.publish(to_web_channel, to_web_faild)
        else:
            logger.info(send.log)


def cloud_setting(device_sn):
    device_socket = sockets_controller.get_socket(device_sn)

    if not device_socket:
        logger.info('cannot find the device:{device} to update setting'.format(device=device_sn))
    else:
        logger.info('get the tcp_socket:' + device_sn)

        content = collections.OrderedDict()
        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=device_sn).first()

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
            content['justification'] = device.justification
            content['add_qr'] = device.add_qr

            if device.ip_white_list:
                content['ip_white_list'] = json.loads(device.ip_white_list)

            if device.bluetooth_white_list:
                content['bluetooth_white_list'] = json.loads(device.bluetooth_white_list)

            if device.order_invalid_keys:
                content['order_invalid_keys'] = json.loads(device.order_invalid_keys)

            if device.order_valid_keys:
                content['order_valid_keys'] = json.loads(device.order_valid_keys)

            if device.cut_cmds:
                content['cut_cmds'] = json.loads(device.cut_cmds)

        send = push_data(device_sn,'update_setting',10,content)
        try:
            device_socket.send(send.data)
        except Exception, e:
            logger.error(e)
            logger.info('can not send {device} for device setting'.format(device=device_sn))
            sockets_controller.pop_socket(device_sn)
        else:
            logger.info(send.log)


def device_update_app(web_data):
    device_sn = web_data.get('device_sn')
    newest_url = web_data.get('newest_url')
    device_socket = sockets_controller.get_socket(device_sn)

    if not device_socket:
        logger.info('cannot find the device:{device} to update app'.format(device=device_sn))
    else:
        logger.info('ready to update app, get the tcp_socket:' + device_sn)
        content = collections.OrderedDict()
        content['newest_url'] = newest_url
        update_send = push_data(device_sn,'update_app',12,content)
        try:
            device_socket.send(update_send.data)
        except Exception, e:
            logger.error(e)
            logger.info('can not send to the {device}'.format(device=device_sn))
            sockets_controller.pop_socket(device_sn)
        else:
            logger.info(update_send.log)


def receive_web_redis_publish():
    while True:
        ps = redis_web_device.pubsub()
        ps.subscribe(['cmd_print', 'cmd_setting', 'cmd_update_app'])
        for item in ps.listen():
            if item['type'] == 'message' and item['channel'] == 'cmd_print':
                data_str = item['data']
                try:
                    data = eval(data_str)
                    logger.info(data)
                except Exception, e:
                    logger.error(e)
                else:
                    cloud_print(data)

            if item['type'] == 'message' and item['channel'] == 'cmd_setting':
                data_str = item['data']
                try:
                    data = eval(data_str)
                    logger.info(data)
                except Exception, e:
                    logger.error(e)
                else:
                    device_sn = data.get('device_sn')
                    cloud_setting(str(device_sn))

            if item['type'] == 'message' and item['channel'] == 'cmd_update_app':
                data_str = item['data']
                try:
                    data = eval(data_str)
                    logger.info(data)
                except Exception, e:
                    logger.error(e)
                else:
                    device_update_app(data)
        gevent.sleep(0)


def received_update_token(data,tcp_socket):
    content = data.get('content')
    if type(content) == type(''):
        content = eval(content)
    key = content.get('key')
    store_token = hashlib.md5(tcp_socket.device_sn + key).hexdigest()
    r_upload_token.set(tcp_socket.device_sn, store_token)

