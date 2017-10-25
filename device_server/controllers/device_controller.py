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
from super_models.history_model import EventsHistroy
from super_models.store_model import Store
from super_models.device_key_model import DeviceKey
import random,string,hashlib,traceback

def pre_connect(data,tcp_socket):
    token = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    tcp_socket.aes_key = token
    content ={}
    content['token'] = token
    send = succss_response_content(tcp_socket.device_sn,data,content)
    try:
        tcp_socket.send(send.data)
    except Exception, e:
        logger.error(e)
    else:
        logger.info(send.log)

def init_connect(data,tcp_socket,sockets):
    seq = data.get('seq')
    content = data.get('content')

    version = data.get('version')
    tcp_socket.version = int(version)

    sign = content.get('sign')

    key_session = Session()
    if tcp_socket.version > 4:
        device_sn = content.get('device_sn')
        if not device_sn:
            logger.info('this device no device_sn,can\'t sign')
            tcp_socket.close()
            return

        try:
            key_model = key_session.query(DeviceKey).filter_by(device_sn=device_sn).first()
        except Exception,e:
            logger.error(e)
        else:
            my_sign = ''
            if key_model:
                pre = key_model.key + tcp_socket.aes_key + device_sn
                hash_pre = hashlib.md5(pre.encode('utf-8')).hexdigest()
                second_key = hash_pre[:16]
                tcp_socket.aes_key = second_key
                my_sign = second_key[:10]
                my_sign = hashlib.md5(my_sign.encode('utf-8')).hexdigest()
            else:
                logger.info('{device} can not find the key'.format(device=device_sn))

            if my_sign != sign:
                logger.info('{device} sign failed,the sign not correct'.format(device=device_sn))
                send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Sign_Valid)
                try:
                    tcp_socket.send(send.data)
                except Exception, e:
                    logger.error(e)
                else:
                    logger.info(send.log)
                finally:
                    tcp_socket.close()
                return
            else:
                tcp_socket.device_sn = device_sn
                logger.info('{device} sign success'.format(device=device_sn))
        finally:
            key_session.close()
    else:
        try:
            opensign = b64_aes_dec(sign)
        except Exception,e:
            logger.error(e)
            send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Sign_Valid)
            try:
                tcp_socket.send(send.data)
            except Exception, e:
                logger.error(e)
            else:
                logger.info(send.log)
            return


        logger.debug('opensign:'+opensign)
        random_num,device_sn = opensign.split('|')

        if not device_sn:
            logger.info('init information incorrect, close the socket')
            tcp_socket.close()
            return
        else:
            tcp_socket.device_sn = device_sn
            logger.info('{device_sn} init connect'.format(device_sn=device_sn))

        if device_sn == '6201001000006':
            logger.error('this is a test error for the device 6201001000006')

    local_setting_version = content.get('local_setting_version')
    app_version = content.get('app_version')
    wifi_list = content.get('wifi_list')

    if not app_version:
        app_version = ''

    device_session = Session()
    try:
        device = device_session.query(Device).filter_by(sn=device_sn).first()
    except Exception,e:
        logger.error(e.message)
        send = fail_response(tcp_socket.device_sn, data, errors.ERROR_No_Such_Device)
        try:
            tcp_socket.send(send.data)
        except Exception, e:
            logger.error(e)
        else:
            logger.info(send.log)
        tcp_socket.close()
    else:
        if not device:
            send = fail_response(tcp_socket.device_sn,data,errors.ERROR_No_Such_Device)
            try:
                tcp_socket.send(send.data)
            except Exception, e:
                logger.error(e)
            else:
                logger.info(send.log)
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
            content['add_qr'] = device.add_qr
            content['justification'] = device.justification

            if device.logo_new:
                if device.logo_urls:
                    content['logo_urls'] = json.loads(device.logo_urls)
                device.logo_new = False
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

            send = succss_response_content(tcp_socket.device_sn,data,content)

            try:
                tcp_socket.send(send.data)
            except Exception,e:
                logger.error(e)
            else:
                logger.info(send.log)

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

            # 将device存到数据库
            try:
                device_session.commit()
            except Exception,e:
                logger.error(e)
    finally:
        device_session.close()


def heart_beat(data,tcp_socket):
    content = data.get('content')
    changed = content.get('changed')
    if changed:
        port_connecting = content.get('port_connecting')
        # device_state = content.get('device_state')
        # network_state = content.get('network_state')

        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=tcp_socket.device_sn).first()
            if not device:
                logger.info('no device,close the tcp socket')
                tcp_socket.close()
                return
            device.port_connecting = port_connecting
            if not port_connecting:
                history = EventsHistroy()
                history.device_sn = tcp_socket.device_sn
                history.time = int(time.time())
                history.start_time = int(time.time())
                history.type = 2
                history.status = 0
                store = session.query(Store).filter(Store.store_id==Device.store_id,Device.sn==tcp_socket.device_sn).first()
                if store:
                    history.store_id = store.store_id
                    history.store_name = store.name

                session.add(history)
            session.commit()
    send = success_response(tcp_socket.device_sn,data)
    device_sn = tcp_socket.device_sn
    device_redis.update_online_device(device_sn)
    try:
        tcp_socket.send(send.data)
    except Exception, e:
        logger.error(e)
    else:
        logger.info(send.log)


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
    send = succss_response_content(tcp_socket.device_sn,data,content)
    try:
        tcp_socket.send(send.data)
    except Exception, e:
        logger.error(e)
    else:
        logger.info(send.log)



def position_report(data,tcp_socket):
    send = success_response(tcp_socket.device_sn,data)
    try:
        tcp_socket.send(send.data)
    except Exception, e:
        logger.error(e)
    else:
        logger.info(send.log)


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
        logger.error(e)
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




