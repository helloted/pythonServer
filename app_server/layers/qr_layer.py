import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from flask import Blueprint
from app_server.utils.request_handle import request_unpack,login_required
from flask import request
from super_models.order_model import Order
from super_models.lottery_model import Lottery
from super_models.store_model import Store
from app_server.response import errors
from app_server.models import SessionContext
from super_models.database import Session
from app_server.response import success_resp,failed_resp,errors
from log_util.app_logger import logger
import random,time

node_qr=Blueprint('qr_layer',__name__,)


def lottery_random():
    num = random.randint(1, 3)
    lottery_type = 0
    if num == 0:
        content = 'Nothing'
        info = 'Sorry, you got nothing, please try it next time'
    elif num == 1:
        lottery_type = 1
        content = '200M'
        info = 'Congratulations, you won Mobile Data {content}'.format(content=content)
    elif num == 2:
        lottery_type  = 1
        content = '100M'
        info = 'Congratulations, you won Mobile Data {content}'.format(content=content)
    else:
        lottery_type = 1
        content = '50M'
        info = 'Congratulations, you won Mobile Data  {content}'.format(content=content)
    return num,lottery_type,content,info


@node_qr.route('/scan', methods=['POST'])
@request_unpack
@login_required
def qr_scan(body):
    order_sn = body.get('order_sn')
    if not order_sn:
        resp = failed_resp(errors.ERROR_Parameters)
        logger.info(resp.log)
        return resp.data
    user_id = request.args.get('user_id')
    with SessionContext() as session:
        order = session.query(Order).filter(Order.order_sn==order_sn).first()
        if not order:
            resp = failed_resp(errors.ERROR_QRCode_Invalid)
            logger.info(resp.log)
            return resp.data

        lottery = session.query(Lottery).filter(Lottery.order_sn==order_sn).first()
        if lottery:
            resp = failed_resp(errors.ERROR_QRCode_Repeated)
            logger.info(resp.log)
            return resp.data
        else:
            lottery = Lottery()
            num,lottery_type,content,info = lottery_random()
            lottery.user_id = user_id
            lottery.lottery_status = num
            lottery.lottery_content = content
            lottery.lottery_info = info
            lottery.order_sn = order_sn
            lottery.lottery_type = lottery_type
            lottery.lottery_time = int(round(time.time() * 1000))
            lottery.order_time = order.order_time
            data = {}
            for key, value in vars(lottery).items():
                if key == 'id' or key == '_sa_instance_state':
                    continue
                data[key] = value
            session.add(lottery)
            session.commit()
            session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_qr.route('/list', methods=['GET'])
@request_unpack
@login_required
def qr_list():
    paras = request.args
    user_id = paras.get('user_id')
    page = paras.get('page')
    amount = paras.get('amount')
    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int-1) * amount_int
    data = []
    with SessionContext() as session:
        lotterrys = session.query(Lottery).order_by((Lottery.lottery_time.desc())).filter(Lottery.user_id==user_id).limit(amount_int).offset(offset).all()
        if lotterrys:
            for lot in lotterrys:
                lot_dict = {}
                for key, value in vars(lot).items():
                    if key == 'id' or key == '_sa_instance_state':
                        continue
                    lot_dict[key] = value
                data.append(lot_dict)
        session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data


