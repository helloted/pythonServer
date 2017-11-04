#coding=utf-8
from celery import Celery
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import time,imp,traceback
from convert_server.logger import logger
from super_models.deal_model import Deal
from super_models.database import Session
import json
from datetime import datetime
from super_models.device_model import Device
from super_models.deal_status_model import DealStatus
from redis_manager import redis_center
from super_models.order_model import Order
from super_models.device_store_model import DeviceStore


broker_url = 'redis://localhost:6379/10'
backend_url = 'redis://localhost:6379/11'

app = Celery('convert_deal', backend=backend_url, broker=broker_url)


@app.task
def receive(msg):
    try:
        msg_dict = json.loads(msg)
    except Exception,e:
        logger.error(e)
        logger.error('json_to_dict error, {msg}'.format(msg=msg))
    else:
        device_sn = msg_dict['device_sn']
        deal_sn = msg_dict['deal_sn']
        content = msg_dict['content']

        if deal_sn and content and device_sn:
            logger.info('Received: {device_sn}, {deal_sn},{content}'.format(device_sn=device_sn,deal_sn=deal_sn,content=content))
            convert(device_sn,deal_sn,content)
            return 'pass success'
        else:
            logger.error('para missing')
            return 'para missing'


def convert(device_sn,deal_sn,content):
    # 搜寻解析脚本
    superPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    folderPath = superPath + '/conversion_scripts/'
    script_name = 's_{device_sn}.py'.format(device_sn=device_sn)
    script_path = folderPath + script_name

    try:  # 判断是否存在脚本
        py_module = imp.load_source('s_{device_sn}'.format(device_sn=device_sn), script_path)
    except Exception,e:
        logger.error(e)
        logger.error('{deal_sn} load script {script} failed'.format(deal_sn=deal_sn,script=script_name))
        convert_failed_handle(deal_sn, content)
    else:
        try:  # 小票单开始解析
            result_dict = py_module.format_convert(content)
        except Exception:
            logger.error(traceback.format_exc())
            logger.error('{deal_sn} convert error'.format(deal_sn=deal_sn))
            convert_failed_handle(deal_sn, content)
        else:
            if not result_dict:
                logger.error('{deal_sn} convert failed, no result return'.format(deal_sn=deal_sn))
                convert_failed_handle(deal_sn, content)
                return

            logger.info(result_dict)

            status = result_dict.get('status')
            order_type = result_dict.get('orderType')

            if status: # 解析成功
                logger.info('{deal_sn} convert success,order_type is {order_type}'.format(deal_sn=deal_sn, order_type=order_type))
                update_deal_status(deal_sn,1,order_type)
                if order_type == 1: # 点菜单,需要保存进数据库
                    try:
                        save_deal_to_DB(device_sn, deal_sn, result_dict)
                        save_order_to_DB(device_sn,deal_sn, result_dict)
                    except Exception, e:
                        logger.error(e)
                        logger.info('save {deal_sn} to DB error'.format(deal_sn=deal_sn))
                        save_convert_failed_file(deal_sn, content)
            else: # 解析失败
                logger.error('{deal_sn} convert finish, but result status is False'.format(deal_sn=deal_sn))
                convert_failed_handle(deal_sn, content)


def convert_failed_handle(deal_sn,content):
    save_convert_failed_file(deal_sn, content)
    update_deal_status(deal_sn, 2)


def update_deal_status(deal_sn,status,type=None):
    session = Session()
    try:
        deal_status = session.query(DealStatus).filter(DealStatus.deal_sn==deal_sn).first()
    except Exception,e:
        logger.error(e)
    else:
        if deal_status:
            now_msec = int(round(time.time() * 1000))
            deal_status.status = status
            deal_status.handle_time = now_msec
            deal_status.deal_type = type

            try:
                session.commit()
            except Exception,e:
                logger.error(e)
        else:
            logger.error('{deal_sn} does not found status record')
    finally:
        session.close()


def save_convert_failed_file(deal_sn,content):
    super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    folder_path = super_path + '/files/convert_failed/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = folder_path+deal_sn+'.txt'

    if isinstance(content, (dict)):
        content = json.dumps(content)
    try:
        fh = open(file_path, 'w')
        fh.write(content)
        fh.close()
    except Exception,e:
        logger.error(e)
    else:
        logger.info('{deal_sn} convert failed,saved at {path}'.format(deal_sn=deal_sn,path=file_path))


def save_deal_to_DB(device_sn,deal_sn,convert_result):
    origin_id = convert_result.get('order_id')
    origin_id_ok = db_check_originID_is_ok(device_sn,deal_sn,origin_id)
    if not origin_id_ok:
        return

    store_id,store_name = db_get_deal_store_info(device_sn)
    if not store_id:
        store_id = -1
    if not store_name:
        store_name = 'NoStore'


    logger.info(store_id)

    session = Session()
    try:
        deal = session.query(Deal).filter(Deal.sn==deal_sn).first()
    except Exception,e:
        logger.error(e)
    else:
        if not deal:
            deal = Deal()
            session.add(deal)

        total_price = convert_result.get('total_price')
        if not total_price:
            total_price=0

        items_list = convert_result.get('items_list')
        if not items_list:
            items_list = []

        deal.sn = convert_result.get('sn')
        deal.time = convert_result.get('time')
        deal.tax = convert_result.get('tax')
        deal.orgin = convert_result.get('orgin')
        deal.store_id = store_id
        deal.store_name = store_name

        deal.device_sn = device_sn
        deal.total_price = int(total_price)
        deal.items_list = json.dumps(items_list)
        deal.orgin_id = origin_id

        if not deal.time:
            deal.time = 0
        deal.datetime = datetime.fromtimestamp(int(int(deal.time)/1000))

        try:
            session.commit()
        except Exception, e:
            session.rollback()
            logger.error(e.message)
        else:
            logger.info('save deal {sn} to DB  success'.format(sn=deal_sn))
            # 发送广播
            live = {}
            live['store_id'] = store_id
            live['device_sn'] = device_sn
            live['deal_sn'] = deal.sn
            live['time'] = deal.time
            live['total_price'] = total_price
            live['tax'] = deal.tax
            live['orgin_id'] = deal.orgin_id

            channel = 'live_deal' + str(store_id)

            redis_center.publish(channel, live)
    finally:
            session.close()


def db_check_originID_is_ok(device_sn,deal_sn,origin_id):
    # 根据原单ID来去重
    if not origin_id:
        logger.info('{deal_sn} convert_result no origin_id,do not save this deal'.format(deal_sn=deal_sn))
        return False
    else:
        check_session = Session()
        try:
            old_deal = check_session.query(Deal).filter_by(orgin_id=origin_id).first()
        except Exception,e:
            logger.error(e)
        else:
            if old_deal and old_deal.device_sn==device_sn and old_deal.sn != deal_sn:
                logger.info('same_order_id:{origin_id}'.format(origin_id=origin_id))
                return False
            else:
                return True
        finally:
            check_session.close()


def db_get_deal_store_info(device_sn):
    session = Session()
    try:
        device_store = session.query(DeviceStore).filter(DeviceStore.device_sn==device_sn).first()
    except Exception,e:
        logger.error(e)
        return None,None
    else:
        if device_store:
            return device_store.store_id,device_store.store_name
        else:
            return None,None
    finally:
        session.close()


def save_order_to_DB(device_sn,deal_sn,convert_result):
    order_sn = deal_sn
    original_id = convert_result.get('order_id')
    origin_id_ok = check_order_id_is_OK(device_sn,order_sn,original_id)
    if not origin_id_ok:
        return

    store_id,store_name = db_get_deal_store_info(device_sn)
    if not store_id:
        store_id = -1
    if not store_name:
        store_name = 'NoStore'

    total_price = convert_result.get('total_price')
    if not total_price:
        total_price = 0

    items_list = convert_result.get('items_list')
    if not items_list:
        items_list = []

    order_time = convert_result.get('time')
    if not order_time:
        order_time = int(time.time()) * 1000
    tax = convert_result.get('tax')
    original_text = convert_result.get('orgin')
    remark = convert_result.get('remark')

    session = Session()
    try:
        order = session.query(Order).filter(Order.order_sn==order_sn).first()
    except Exception,e:
        logger.error(e)
    else:
        if not order:
            order = Order()
            session.add(order)

        order.order_sn = order_sn
        order.device_sn = device_sn
        order.order_time = order_time
        order.total_price = total_price
        order.tax = tax
        order.items_list = json.dumps(items_list)
        order.original_id = original_id
        order.original_text = original_text
        order.store_id = store_id
        order.store_name = store_name
        if remark:
            order.remark = remark

        try:
            session.commit()
        except Exception, e:
            session.rollback()
            logger.error(e.message)
        else:
            logger.info('save order {sn} to DB  success'.format(sn=order_sn))
    finally:
        session.close()


def check_order_id_is_OK(device_sn,order_sn,original_id):
    # 根据原单ID来去重
    if not original_id:
        logger.info('{deal_sn} convert_result no origin_id,do not save this deal'.format(deal_sn=order_sn))
        return False
    else:
        check_session = Session()
        try:
            old_order = check_session.query(Order).filter(Order.original_id==original_id).first()
        except Exception,e:
            logger.error(e)
            return False
        else:
            if old_order and old_order.device_sn == device_sn and old_order.order_sn != order_sn: # 属于复盘单
                logger.info('{deal_sn} convert_result has repeat order id {original_id},ignore this order'.format(
                    deal_sn=order_sn, original_id=original_id))
                return False
            else:
                return True
        finally:
            check_session.close()