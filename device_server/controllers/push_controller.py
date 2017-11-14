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

        # 更新设备设置
        if task_type == 'device_setting':
            cloud_setting(task_dict)

        # 更新设备设置
        if task_type == 'interactive_setting':
            interactive_setting(task_dict)

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


def cloud_setting(task_dict):
    device_sn = task_dict.get('device_sn')
    msg_sn = task_dict.get('msg_sn')
    cmd = 'update_setting'
    seq = 18
    msg_content = task_dict.get('content')
    content = collections.OrderedDict()
    content['msg_sn'] = msg_sn
    content['device_sn'] = device_sn
    with SessionContext() as session:
        device = session.query(Device).filter_by(sn=device_sn).first()

        for key in msg_content:
            if key and not msg_content[key]:
                continue
            if key == 'bluetooth_white_list' or key == 'ip_white_list' or key == 'cut_cmds' or key == 'order_invalid_keys' or key == 'order_valid_keys':
                device.__setattr__(key, json.dumps(msg_content[key]))
            else:
                device.__setattr__(key, msg_content[key])
        device.setting_time = int(time.time())

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
        session.commit()

    push_to_device_handle(device_sn=device_sn, cmd=cmd, content=content, seq=seq, msg_sn=msg_sn)


def interactive_setting(task_dict):
    msg_sn = task_dict.get('msg_sn')
    device_sn = task_dict.get('device_sn')
    url = task_dict.get('url')
    url_type = task_dict.get('url_type')

    content = {}
    content['device_sn'] = device_sn
    content['url'] = url
    content['type'] = url_type
    cmd = 'interactive_setting'
    seq = 20

    push_to_device_handle(device_sn=device_sn, cmd=cmd, content=content, seq=seq, msg_sn=msg_sn)


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







