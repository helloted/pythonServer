#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.11.04
设备资料
"""

from flask import Blueprint
from flask import request
from super_models.device_model import Device
from web_server.models import SessionContext
from web_server.utils.handles import transfer
from web_server.utils.response import response_success,response_failed
from log_util.web_demo_logger import logger
from web_server.utils import errors
from super_models.device_store_model import DeviceStore
from redis_manager import device_redis
import json
from super_models.store_model import Store


node_device_info=Blueprint('device_info_layer',__name__,)


@node_device_info.route('/list', methods=['GET'])
@transfer
def device_list():
    page = request.args.get('page')
    amount = request.args.get('amount')

    if not page or not amount:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int - 1) * amount_int

    with SessionContext() as session:
        devices = session.query(Device).limit(amount_int).offset(offset).all()
        total = session.query(Device).count()
        data = {}
        total_page = total / amount_int + 1
        data['page_total'] = total_page
        data['current_page'] = page_int
        data['amount'] = amount_int
        device_list = []
        for dev in devices:
            device = {}
            device['device_sn'] = dev.sn

            device_store = session.query(DeviceStore).filter(DeviceStore.device_sn == dev.sn).first()
            if device_store:
                device['store_id'] = device_store.store_id
                device['store_name'] = device_store.store_name
            else:
                device['store_id'] = 0
                device['store_name'] = 'no store'

            device['online'] = device_redis.check_online(dev.sn)

            device['problem'] = False
            device_list.append(device)
        data['devices'] = device_list
        session.result = response_success(data)

    logger.info(session.result.log)
    return session.result.resp_data


@node_device_info.route('/detail', methods=['GET'])
@transfer
def device_detail():
    device_sn = request.args.get('device_sn')
    if not device_sn:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    with SessionContext() as session:
        device = session.query(Device).filter_by(sn=device_sn).first()
        data = {}
        if device:
            data['device_sn'] = device.sn
            data['problem'] = device.problem
            data['phone'] = device.phone
            data['wifi_name'] = device.wifi_name
            data['wifi_password'] = device.wifi_password
            data['wifi_encrypt_type'] = device.wifi_encrypt_type
            data['capture_baudrate'] = device.capture_baudrate
            data['app_print_baudrate'] = device.app_print_baudrate
            data['app_received_baudrate'] = device.app_received_baudrate
            data['net_port'] = device.net_port
            data['app_version'] = device.app_version
            data['port_connecting'] = device.port_connecting
            data['add_qr'] = device.add_qr
            data['justification'] = device.justification

            wifi_list = device.wifi_list
            data['wifi_list'] = []
            if wifi_list:
                data['wifi_list'] = json.loads(wifi_list)

            device_store = session.query(DeviceStore).filter(DeviceStore.device_sn == device.sn).first()
            if device_store:
                data['store_id'] = device_store.store_id
                data['store_name'] = device_store.store_name
            else:
                data['store_id'] = 0
                data['store_name'] = 'no store'

            last_time = device_redis.get_last_online_time(device.sn)
            if not last_time:
                last_time = 0
            data['last_online_time'] = last_time

            if device.bluetooth_white_list:
                data['bluetooth_white_list'] = json.loads(device.bluetooth_white_list)
            else:
                data['bluetooth_white_list'] = None

            if device.ip_white_list:
                data['ip_white_list'] = json.loads(device.ip_white_list)
            else:
                data['ip_white_list'] = None

            if device.cut_cmds:
                data['cut_cmds'] = json.loads(device.cut_cmds)
            else:
                data['cut_cmds'] = None

            if device.order_valid_keys:
                data['order_valid_keys'] = json.loads(device.order_valid_keys)
            else:
                data['order_valid_keys'] = None

            if device.order_invalid_keys:
                data['order_invalid_keys'] = json.loads(device.order_invalid_keys)
            else:
                data['order_invalid_keys'] = None

            session.result = response_success(data)

    logger.info(session.result.log)
    return session.result.resp_data


@node_device_info.route('/filter', methods=['OPTIONS','POST'])
@transfer
def device_filter(body):
    page = body.get('page')
    amount = body.get('amount')
    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int - 1) * amount_int

    device_sn = body.get('device_sn')

    problem = body.get('problem')
    store_name = body.get('store_name')
    has_online = body.has_key('online')

    with SessionContext() as session:
        data = {}
        query = session.query(Device)

        if store_name:
            like_name = '%{name}%'.format(name=store_name)
            query = query.filter(DeviceStore.store_name.ilike(like_name), Device.sn == DeviceStore.device_sn)

        if problem:
            query = query.filter_by(problem=problem)


        if device_sn:
            like_sn = '%{device_sn}%'.format(device_sn=device_sn)
            query = query.filter(Device.sn.ilike(like_sn))

        if has_online:
            online = body.get('online')
            online_list = device_redis.get_online_devices()
            if online:
                query = query.filter(Device.sn.in_(online_list))
            else:
                query = query.filter(~Device.sn.in_(online_list))

        query = query.limit(amount_int).offset(offset)

        devices = query.all()
        total = len(devices)

        total_page = total / amount_int + 1
        data['page_total'] = total_page
        data['current_page'] = page_int
        data['amount'] = amount_int

        device_list = []
        for dev in devices:
            device = {}
            device['device_sn'] = dev.sn

            device_store = session.query(DeviceStore).filter(DeviceStore.device_sn == dev.sn).first()
            if device_store:
                device['store_id'] = device_store.store_id
                device['store_name'] = device_store.store_name

            device['online'] = device_redis.check_online(dev.sn)

            device['problem'] = False
            device_list.append(device)

        data['devices'] = device_list
        session.result = response_success(data)

    logger.info(session.result.log)
    return session.result.resp_data


@node_device_info.route('/bind_store', methods=['OPTIONS','POST'])
@transfer
def bind_store(body):
    store_id = body.get('store_id')
    device_sn = body.get('device_sn')
    logger.info(device_sn)
    with SessionContext() as session:
        bind = session.query(DeviceStore).filter(DeviceStore.device_sn==device_sn).first()
        logger.info(bind)
        if not bind:
            session.result = response_failed(errors.ERROR_No_Such_Deivce)
        else:
            bind.store_id = store_id
            store = session.query(Store).filter(Store.store_id==store_id).first()
            if not store:
                session.result = response_failed(errors.ERROR_No_Such_Store)
            else:
                bind.store_name = store.name
                session.commit()
                session.result = response_success()
    logger.info(session.result.log)
    return session.result.resp_data