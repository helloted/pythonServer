from flask import Blueprint
from app_server.utils.request_handle import request_unpack,login_required
from flask import request
from super_models.order_model import Order
from super_models.lottery_model import Lottery
from app_server.response import errors
from app_server.models import SessionContext
from app_server.response import success_resp,failed_resp,errors
from log_util.app_logger import logger
import random,time

node_qr=Blueprint('qr_layer',__name__,)


def lottery_random():
    num = random.randint(0, 3)
    if num == 0:
        content = 'Sorry, you got nothing, please try it next time'
    elif num == 1:
        content = 'Congratulations, you won Mobile Data 200M'
    elif num == 2:
        content = 'Congratulations, you won Mobile Data 100M'
    else:
        content = 'Congratulations, you won Mobile Data 50M'
    return num,content


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
            num,content = lottery_random()
            lottery.user_id = user_id
            lottery.lottery_status = num
            lottery.lottery_content = content
            lottery.order_sn = order_sn
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

