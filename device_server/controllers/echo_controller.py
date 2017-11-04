#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.11.01
Device应答的处理
"""

from redis_manager import redis_web_device
import json
from log_util.device_logger import logger
import time


def echo_push_handle(data,tcp_socket):
    content = data.get('content')
    code = content.get('code')
    msg_sn = content.get('msg_sn')
    if code == 0 and msg_sn:

        success_push(tcp_socket.device_sn,msg_sn)


def success_push(device_sn,msg_sn):
    msg_dict = {'msg_sn': msg_sn,'code':0}
    msg = json.dumps(msg_dict)
    channel_name = 'channel_device_pub_web' + str(device_sn)
    redis_web_device.publish(channel_name, msg)


def publish_cannot_find_device(device_sn,msg_sn):
    msg_dict = {'msg_sn': msg_sn,'code':1}
    msg = json.dumps(msg_dict)
    channel_name = 'channel_device_pub_web' + str(device_sn)
    redis_web_device.publish(channel_name, msg)

