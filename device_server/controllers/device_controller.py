#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.01
设备处理
"""

from super_models.device_model import Device, SeedToken
from super_models.database import Session
from log_util.device_logger import logger
from device_server.utils.comment import b64_aes_dec, aes_enc_b64, token_random
import collections
import json
from device_server.response.res import success_response,succss_response_content, fail_response
from device_server.response import errors
from gevent._socket2 import _closedsocket
import sockets_controller
import redis_manager.device_redis as device_redis
import time,os
from device_server.db_tool import SessionContext

def init_connect(data,tcp_socket,sockets):
    seq = data.get('seq')
    content = data.get('content')
    sign = content.get('sign')

    local_setting_version = content.get('local_setting_version')
    app_version = content.get('app_version')

    wifi_list = content.get('wifi_list')

    if not app_version:
        app_version = ''

    try:
        opensign = b64_aes_dec(sign)
    except Exception,e:
        jsonrsp = fail_response(101, 'base64'+str(e), seq)
        return None,jsonrsp

    logger.debug('opensign:'+opensign)

    random_num,serial_num = opensign.split('|')

    session = Session()

    try:
        device = session.query(Device).filter_by(sn=serial_num).first()
    except Exception,e:
        session.rollback()
        logger.info(e.message)
        send = fail_response(seq,errors.ERROR_No_Such_Device)
        tcp_socket.send(send)
        tcp_socket.close()
    else:
        if not device:
            send = fail_response(seq,errors.ERROR_No_Such_Device)
            tcp_socket.send(send)
            tcp_socket.close()
        else:
            tcp_socket.device_sn = device.sn
            tcp_socket.store_id = device.store_id

            content = {}
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
            content['newest_url'] = device.newest_url
            if device.ip_white_list:
                content['ip_white_list'] = json.loads(device.ip_white_list)

            if device.bluetooth_white_list:
                content['bluetooth_white_list'] = json.loads(device.bluetooth_white_list)
            send = succss_response_content(data,content)
            tcp_socket.send(send)

            sockets_controller.set_socket(device.sn,tcp_socket)

            # 加入在线socket列表
            key = 'socket' + device.sn

            old_socket = sockets.get(key)
            if old_socket and not isinstance(tcp_socket._sock, _closedsocket):
                old_socket.close()
                logger.info('old device {sn} has closed,the new one update'.format(sn=device.sn))

                device_redis.update_online_device(device.sn)

            sockets[key] = tcp_socket

            device.app_version = app_version
            if local_setting_version:
                device.local_setting_version = local_setting_version
            if wifi_list:
                device.wifi_list = json.dumps(wifi_list)
            session.commit()
    finally:
        session.close()
        logger.info(send)


def heart_beat(data,tcp_socket):
    content = data.get('content')
    changed = content.get('changed')
    if changed:
        port_connecting = content.get('port_connecting')
        device_state = content.get('device_state')
        network_state = content.get('network_state')

        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=tcp_socket.device_sn).first()
            device.port_connecting = port_connecting
            device.device_state = device_state
            device.network_state = network_state

            session.commit()

    send = success_response(data)
    device_sn = tcp_socket.device_sn
    device_redis.update_online_device(device_sn)
    try:
        tcp_socket.send(send)
    except Exception,e:
        logger.error(e.message)
    else:
        logger.info(send)


def request_app(data,tcp_socket):
    superpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,os.pardir))
    folder = superpath + '/files/app'
    file_list = os.listdir(folder)
    temp = ''
    temp_time = 0
    for file in file_list:
        current_time = int(os.path.getctime(folder + '/' + file))
        if current_time > temp_time:
            temp_time = current_time
            temp = file
    content = {}
    content['url'] = 'http://47.74.130.48:8005/files/app/' + temp
    send = succss_response_content(data,content)
    tcp_socket.send(send)
    logger.info(send)



def position_report(data,tcp_socket):
    send = success_response(data)
    tcp_socket.send(send)
    logger.info(send)


def pushToken():
    token = token_random()

    result = token[:10]

    session = Session()

    seed_token = SeedToken()
    seed_token.token = result

    session.add(seed_token)

    try:
        session.commit()
        print 'success login'
    except Exception, e:
        session.rollback()
        print 'Exception:',e.message

    enctoken = aes_enc_b64(token)

    dic = collections.OrderedDict()
    dic['cmd'] = 'update_token'
    dic['version'] = '1.0'
    dic['seq'] = 2

    content = collections.OrderedDict()

    content['type'] = 1
    # content['id']
    content['token'] = enctoken

    dic['content'] = content
    jsresp = json.dumps(dic)

    return jsresp




