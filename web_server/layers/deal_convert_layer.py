#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.04
解析失败订单处理
"""

from flask import Blueprint
from flask import request
import os
from super_models.deal_status_model import DealStatus
from super_models.database import Session
from web_server.models import SessionContext
from web_server.utils.handles import transfer
from web_server.utils.response import response_success,response_failed
from web_server.utils import errors
import time,json
from redis_manager import r_queue
from log_util.web_demo_logger import logger
from celery import Celery


node_deal_convert=Blueprint('deal_convert_layer',__name__,)

super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
folder_path = super_path + '/files/convert_failed'


broker_url = 'redis://localhost:6379/10'
backend_url = 'redis://localhost:6379/11'

client = Celery('convert_deal', backend=backend_url, broker=broker_url)


def get_files_info():
    file_list = os.listdir(folder_path)
    data = []
    for file in file_list:
        file_dict = {}
        file_dict['deal_name'] = file
        file_dict['time'] = int(os.path.getctime(folder_path + '/' + file))
        data.append(file_dict)

    return data


@node_deal_convert.route('/list', methods=['GET'])
@transfer
def deal_list():
    data = get_files_info()
    resp = response_success(data)
    logger.info(resp.log)
    return resp.resp_data


@node_deal_convert.route('/event', methods=['POST'])
@transfer
def deal_event(post_body):
    deal_name = post_body.get('deal_name')
    event = post_body.get('event')
    if not deal_name or not event:
        resp = response_failed(errors.ERROR_Para_Error)
        logger.info(resp.log)
        return resp.resp_data

    event = int(event)

    device_sn = deal_name[:13]
    deal_sn = deal_name[:-4]

    file_path = folder_path + '/' + deal_name

    if not os.path.exists(file_path):
        resp = response_failed(errors.ERROR_Deal_Not_Exist)
        logger.info(resp.log)
        return resp.resp_data
    else:
        if event == 1:
            with open(file_path,'r') as file:
                content = file.read()
                os.remove(file_path)
                send_deal_to_celery(device_sn,deal_sn,content)

        if event == 2:
            os.remove(file_path)
            session = Session()
            try:
                deal_status = session.query(DealStatus).filter(DealStatus.deal_sn==deal_sn).first()
            except Exception,e:
                logger.error(e)
            else:
                if deal_status:
                    deal_status.status = 3
                    deal_status.remark = 'Deleted from WEB'
                    session.commit()
            finally:
                session.close()

        data = get_files_info()
        resp = response_success(data)
        logger.info(resp.log)
        return resp.resp_data


def send_deal_to_celery(device_sn,deal_sn,content):
    msg_data = {}
    msg_data['device_sn'] = device_sn
    msg_data['deal_sn'] = deal_sn
    msg_data['content'] = content
    msg_json = json.dumps(msg_data)
    client.send_task('convert_center.receive', (msg_json,))

