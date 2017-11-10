#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.04
WEB服务器Layer处理
"""

from flask import Blueprint
from flask import request
from super_models.device_model import Device
from web_server.models import SessionContext
from web_server.utils.handles import transfer
from web_server.utils.response import response_success,response_failed
import time,json
from redis_manager import r_queue
from log_util.web_demo_logger import logger
from redis_manager import redis_web_device
from web_server.utils import errors

node_device=Blueprint('device_layer',__name__,)


@node_device.route('/qr_info', methods=['GET'])
@transfer
def qr_setting():
    device_sn = request.args.get('device_sn')
    with SessionContext() as session:
        device = session.query(Device).filter_by(sn=device_sn).first()
        if device:
            data = {}
            data['device_sn'] = device_sn
            data['add_qr'] = device.add_qr
            data['qr_keywords'] = []
            if device.qr_keywords:
                data['qr_keywords'] = json.loads(device.qr_keywords)
            session.result = response_success(data)
        else:
            session.result = response_failed(errors.ERROR_No_Such_Deivce)
    logger.info(session.result.log)
    return session.result.resp_data


@node_device.route('/upload_log', methods=['POST','OPTIONS'])
@transfer
def upload_log(post_body):
    device_sn = post_body.get('device_sn')
    log_time = post_body.get('time')

    if not device_sn or not log_time:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    now_msec = int(round(time.time() * 1000))
    send_msg_sn = device_sn + str(now_msec)

    # 先建立监听
    redis_sub = redis_web_device.pubsub()
    channel_name = 'channel_device_pub_web' + str(device_sn)
    redis_sub.subscribe([channel_name,])
    redis_sub.listen()

    data = {}
    data['device_sn'] = device_sn
    data['type'] = 'upload_log'
    data['time'] = log_time
    data['msg_sn'] = send_msg_sn
    r_queue.lpush('devices_queue', data)

    result = wait_for_push_result(channel_name,send_msg_sn,redis_sub)
    logger.info(result.log)
    return result.resp_data


@node_device.route('/repeat_upload_deal', methods=['POST','OPTIONS'])
@transfer
def repeate_upload_deal(post_body):
    device_sn = post_body.get('device_sn')
    start_time = post_body.get('start_time')
    end_time = post_body.get('end_time')

    if not start_time or not end_time or not device_sn:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    now_msec = int(round(time.time() * 1000))
    send_msg_sn = device_sn + str(now_msec)

    # 先建立监听
    redis_sub = redis_web_device.pubsub()
    channel_name = 'channel_device_pub_web' + str(device_sn)
    redis_sub.subscribe([channel_name,])
    redis_sub.listen()

    # 将消息传递给device_server
    data = {}
    data['device_sn'] = device_sn
    data['type'] = 'repeat_upload_deal'
    data['start_time'] = start_time
    data['end_time'] = end_time
    data['msg_sn'] = send_msg_sn
    r_queue.lpush('devices_queue', data)

    result = wait_for_push_result(channel_name,send_msg_sn,redis_sub)
    logger.info(result.log)
    return result.resp_data


@node_device.route('/app_update', methods=['POST','OPTIONS'])
@transfer
def app_update(post_body):
    device_sn = post_body.get('device_sn')
    newest_url = post_body.get('newest_url')

    if not device_sn or not newest_url:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    now_msec = int(round(time.time() * 1000))
    send_msg_sn = device_sn + str(now_msec)

    # 等待device_server回应
    redis_sub = redis_web_device.pubsub()
    channel_name = 'channel_device_pub_web' + str(device_sn)
    redis_sub.subscribe([channel_name,])
    redis_sub.listen()

    # 将消息传递给device_server
    data = {}
    data['device_sn'] = device_sn
    data['type'] = 'app_update'
    data['newest_url'] = newest_url
    data['msg_sn'] = send_msg_sn
    r_queue.lpush('devices_queue', data)

    result = wait_for_push_result(channel_name,send_msg_sn,redis_sub)
    logger.info(result.log)
    return result.resp_data


@node_device.route('/print_content', methods=['POST','OPTIONS'])
@transfer
def print_content(post_body):
    device_sn = post_body.get('device_sn')
    post_time = post_body.get('post_time')
    content = post_body.get('content')

    if not device_sn or not post_time or not content:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    now_msec = int(round(time.time() * 1000))
    send_msg_sn = device_sn + str(now_msec)

    # 先建立监听
    redis_sub = redis_web_device.pubsub()
    channel_name = 'channel_device_pub_web' + str(device_sn)
    redis_sub.subscribe([channel_name,])
    redis_sub.listen()

    # 将消息传递给device_server
    data = {}
    data['type'] = 'print_content'
    data['device_sn'] = device_sn
    data['content'] = content
    data['post_time'] = post_time
    data['msg_sn'] = send_msg_sn
    r_queue.lpush('devices_queue', data)

    result = wait_for_push_result(channel_name,send_msg_sn,redis_sub)
    logger.info(result.log)
    return result.resp_data


@node_device.route('/setting', methods=['POST','OPTIONS'])
@transfer
def device_setting(body):
    device_sn = body.get('device_sn')
    if not device_sn:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    now_msec = int(round(time.time() * 1000))
    send_msg_sn = device_sn + str(now_msec)

    # 先建立监听
    redis_sub = redis_web_device.pubsub()
    channel_name = 'channel_device_pub_web' + str(device_sn)
    redis_sub.subscribe([channel_name,])
    redis_sub.listen()

    # 将消息传递给device_server
    data = {}
    data['type'] = 'device_setting'
    data['device_sn'] = device_sn
    data['content'] = body
    data['msg_sn'] = send_msg_sn
    r_queue.lpush('devices_queue', data)

    result = wait_for_push_result(channel_name,send_msg_sn,redis_sub)
    logger.info(result.log)
    return result.resp_data


def wait_for_push_result(channel_name,send_msg_sn,redis_sub):
    now = int(time.time())
    last_time = 0
    while last_time < 10:
        last_time = int(time.time()) - now
        data = redis_sub.parse_response(block=False, timeout=5)
        if data and data[0] == 'message' and data[1] == channel_name and data[2]:
            content = json.loads(data[2])
            sn = content.get('msg_sn')
            if sn == send_msg_sn:
                code = content.get('code')
                if code == 0:
                    resp = response_success()
                else:
                    resp = response_failed(errors.ERROR_Push_Device_Failed)
                return resp
    resp = response_failed(errors.ERROR_Time_Out_Error)
    return resp