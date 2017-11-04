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
from redis_manager import r_upload_token
import hashlib
from echo_controller import publish_cannot_find_device


keep_socket = None


def receive_push_queue():
    while True:
        task_package = r_queue.brpop('devices_queue', 0)
        task_str = task_package[1]
        task_dict = eval(task_str)
        logger.info('WEB -> HF, {task}'.format(task=task_str))
        task_type = task_dict['type']
        # 上传日志
        if task_type == 'upload_log':
            upload_log(task_dict)

        # 重新上传部分订单
        if task_type == 'repeat_upload_deal':
            repeat_upload_deal(task_dict)

        # 升级APP
        if task_type == 'app_update':
            update_app(task_dict)

        # 打印内容
        if task_type == 'print_content':
            cloud_print(task_dict)

        gevent.sleep(0)


def push_to_device_handle(device_sn,cmd,content,seq,msg_sn=None):
    device_socket = sockets_controller.get_socket(device_sn)
    if not device_socket:
        logger.info('cannot find the device:{device} to {cmd}'.format(device=device_sn,cmd=cmd))
        publish_cannot_find_device(device_sn,msg_sn=msg_sn)
    else:
        send = push_data(device_sn,cmd,seq,content)
        try:
            device_socket.send(send.data)
        except Exception:
            logger.info('can not send {device} for {cmd}'.format(device=device_sn,cmd=cmd))
            publish_cannot_find_device(device_sn, msg_sn=msg_sn)
            sockets_controller.pop_socket(device_sn)
        else:
            logger.info(send.log)


def update_app(task_dict):
    device_sn = task_dict.get('device_sn')
    newest_url = task_dict.get('newest_url')
    msg_sn = task_dict.get('msg_sn')

    content = collections.OrderedDict()
    content['newest_url'] = newest_url
    content['msg_sn'] = msg_sn

    cmd = 'update_app'
    seq = 10
    push_to_device_handle(device_sn=device_sn, cmd=cmd, content=content, seq=seq, msg_sn=msg_sn)


def upload_log(task):
    device_sn = task.get('device_sn')
    time = task.get('time')
    msg_sn = task.get('msg_sn')

    content = {}
    content['time'] = time
    content['msg_sn'] = msg_sn

    cmd = 'upload_log'
    seq = 12
    push_to_device_handle(device_sn=device_sn,cmd=cmd,content=content,seq=seq,msg_sn=msg_sn)


def repeat_upload_deal(task):
    device_sn = task.get('device_sn')
    start_time = task.get('start_time')
    end_time = task.get('end_time')
    msg_sn = task.get('msg_sn')
    content = collections.OrderedDict()
    content['start_time'] = start_time
    content['end_time'] = end_time
    content['msg_sn'] = msg_sn
    cmd = 'repeat_upload_deal'
    seq = 14
    push_to_device_handle(device_sn=device_sn, cmd=cmd, content=content, seq=seq, msg_sn=msg_sn)


def cloud_print(task_dict):
    device_sn = task_dict.get('device_sn')
    post_time = task_dict.get('post_time')
    msg_sn = task_dict.get('msg_sn')
    print_content = task_dict.get('content')

    content = {}
    content['device_sn'] = device_sn
    content['post_time'] = post_time
    content['msg_sn'] = msg_sn
    content['print_content'] = print_content
    cmd = 'print_content'
    seq = 16

    push_to_device_handle(device_sn=device_sn, cmd=cmd, content=content, seq=seq, msg_sn=msg_sn)


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


# def device_update_app(web_data):
#     device_sn = web_data.get('device_sn')
#     newest_url = web_data.get('newest_url')
#     device_socket = sockets_controller.get_socket(device_sn)
#
#     if not device_socket:
#         logger.info('cannot find the device:{device} to update app'.format(device=device_sn))
#     else:
#         logger.info('ready to update app, get the tcp_socket:' + device_sn)
#         content = collections.OrderedDict()
#         content['newest_url'] = newest_url
#         update_send = push_data(device_sn,'update_app',12,content)
#         try:
#             device_socket.send(update_send.data)
#         except Exception, e:
#             logger.error(e)
#             logger.info('can not send to the {device} for update app'.format(device=device_sn))
#             sockets_controller.pop_socket(device_sn)
#         else:
#             logger.info(update_send.log)
#
#
# def device_repeat_upload_deal(web_data):
#     device_sn = web_data.get('device_sn')
#     start_time = web_data.get('start_time')
#     end_time = web_data.get('end_time')
#     msg_sn = web_data.get('msg_sn')
#     device_socket = sockets_controller.get_socket(device_sn)
#
#     if not device_socket:
#         publish_cannot_find_device(device_sn,msg_sn=msg_sn)
#         logger.info('cannot find the device:{device} to repeat_upload_deal'.format(device=device_sn))
#     else:
#         content = collections.OrderedDict()
#         content['start_time'] = start_time
#         content['end_time'] = end_time
#         update_send = push_data(device_sn,'repeat_upload_deal',14,content)
#         try:
#             device_socket.send(update_send.data)
#         except Exception, e:
#             logger.error(e)
#             logger.info('can not send to the {device} for the repeat_upload_deal'.format(device=device_sn))
#             sockets_controller.pop_socket(device_sn)
#         else:
#             logger.info(update_send.log)
#
#
# def receive_web_redis_publish():
#     while True:
#         ps = redis_web_device.pubsub()
#         ps.subscribe(['cmd_print', 'cmd_setting'])
#         for item in ps.listen():
#             if item['type'] == 'message' and item['channel'] == 'cmd_print':
#                 data_str = item['data']
#                 try:
#                     data = eval(data_str)
#                     logger.info(data)
#                 except Exception, e:
#                     logger.error(e)
#                 else:
#                     cloud_print(data)
#
#             if item['type'] == 'message' and item['channel'] == 'cmd_setting':
#                 data_str = item['data']
#                 try:
#                     data = eval(data_str)
#                     logger.info(data)
#                 except Exception, e:
#                     logger.error(e)
#                 else:
#                     device_sn = data.get('device_sn')
#                     cloud_setting(str(device_sn))
#
#             if item['type'] == 'message' and item['channel'] == 'cmd_update_app':
#                 data_str = item['data']
#                 try:
#                     data = eval(data_str)
#                     logger.info(data)
#                 except Exception, e:
#                     logger.error(e)
#                 else:
#                     device_update_app(data)
#         gevent.sleep(0)


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


def received_update_token(data,tcp_socket):
    content = data.get('content')
    if type(content) == type(''):
        content = eval(content)
    key = content.get('key')
    store_token = hashlib.md5(tcp_socket.device_sn + key).hexdigest()
    r_upload_token.set(tcp_socket.device_sn, store_token)







