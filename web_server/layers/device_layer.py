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
from web_server.response.resp import add_headers,success_response,failed_response
import time,json
from redis_manager import r_store_info
from super_models.store_model import Store


node_device=Blueprint('device_layer',__name__,)

@node_device.route('/qr_info', methods=['GET'])
@add_headers
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

            session.result = success_response(data)

        else:
            session.result =  failed_response(3,'no such device')

    return session.result


@node_device.route('/qr_setting', methods=['POST'])
@add_headers
def qr_setting():
    page = request.args.get('page')

    return page

