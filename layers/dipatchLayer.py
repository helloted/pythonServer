#coding=utf-8
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from flask import Blueprint
from flask import request
from response import success_resp,failed_resp
from response import errors
from tools.request_handle import request_unpack
import time
from tools.comment import aes_enc_b64
from models.database import SessionContext
from models.dispatch_model import DispatchModel
from log_util.app_logger import logger
from models.QRmodel import QRModel
from models.product_info_model import ProductInfoModel
import traceback,multiprocessing
from tools.request_handle import request_unpack,web_login_required,web_transfer


node_dispatch=Blueprint('dispatch_layer',__name__,)


@node_dispatch.route('/list', methods=['GET'])
@web_transfer
@web_login_required
def dispatch_list():

    agent_id = request.args.get('agent_id')

    with SessionContext() as session:
        query = session.query(DispatchModel).filter(DispatchModel.status==2)
        if agent_id:
            query = query.filter(DispatchModel.agent_id==int(agent_id))
        d_list = query.all()
        data = []
        for d in d_list:

            d_dict = {}

            d_dict['dispatch_id'] = d.id
            d_dict['dispatch_time'] = d.dispatch_time
            d_dict['count'] = d.count
            d_dict['start_sn'] = d.start_sn
            d_dict['end_sn'] = d.end_sn
            d_dict['agent_id'] = d.agent_id
            d_dict['status'] = d.status

            data.append(d_dict)

        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_dispatch.route('/update', methods=['GET', 'OPTIONS'])
@web_transfer
@web_login_required
def dispatch_update():
    dispatch_id = request.args.get('dispatch_id')
    status = request.args.get('status')

    if not dispatch_id or not status:
        logger.info(failed_resp(errors.ERROR_Parameters).log)
        return failed_resp(errors.ERROR_Parameters).data

    with SessionContext() as session:
        dispatch = session.query(DispatchModel).filter(DispatchModel.id == dispatch_id).first()
        if dispatch:
            dispatch.status = status

            session.query(ProductInfoModel).filter(ProductInfoModel.dispatch_id==dispatch_id).delete()

            session.commit()
            session.result = success_resp()
        else:
            session.result = failed_resp(errors.ERROR_NO_Such_Values)

    logger.info(session.result.log)
    return session.result.data


@node_dispatch.route('/now', methods=['GET'])
@web_transfer
@web_login_required
def dispatch_now():
    start = request.args.get('start_sn')
    end = request.args.get('end_sn')
    to_agent_id = request.args.get('to_agent_id')
    count = request.args.get('count')

    if not start or not end or not to_agent_id or not count:
        resp = failed_resp(errors.ERROR_Parameters)
        logger.info(resp.log)
        return resp.data

    start_int = int(start)
    end_int = int(end)
    need_count = int(count)

    if start_int >= end_int:
        resp = failed_resp(errors.ERROR_Wrong_SN)
        logger.info(resp.log)
        return resp.data

    with SessionContext() as session:
        start_between = session.query(DispatchModel).filter(DispatchModel.status==2).filter((DispatchModel.start_sn <= start_int) & (DispatchModel.end_sn >= start_int)).first()
        end_between = session.query(DispatchModel).filter(DispatchModel.status==2).filter((DispatchModel.start_sn <= end_int) & (DispatchModel.end_sn >= end_int)).first()
        if start_between or end_between:
            session.result = failed_resp(errors.ERROR_Wrong_SN)
        else:
            dispatch = DispatchModel()
            dispatch.start_sn = start_int
            dispatch.end_sn = end_int
            dispatch.agent_id = to_agent_id
            dispatch.count = int(count)
            dispatch.dispatch_time = int(time.time())
            dispatch.status = 1

            session.add(dispatch)
            session.commit()

            data = {'dispatch_id':dispatch.id}

            # 新开进程去设置信息
            p = multiprocessing.Process(target=dispath_qr, args=(start_int, need_count, dispatch.id))
            p.start()

            session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data


def dispath_qr(start_sn,count,dispatch_id):
    with SessionContext() as session:
        try:
            # 批量执行
            inter = 100
            temp = 0
            for i in xrange(count):
                if temp < inter:
                    temp += 1
                else:
                    update_qr(dispatch_id,start_sn,start_sn+temp-1)
                    start_sn = start_sn + temp
                    temp = 1
            update_qr(dispatch_id, start_sn, start_sn + temp - 1)
        except Exception,e:
            logger.error(traceback.format_exc())
        else:
            logger.info('dispatch success dispatch_id:{sn}'.format(sn=dispatch_id))
            dis = session.query(DispatchModel).filter(DispatchModel.id==dispatch_id).first()
            if dis:
                dis.status = 2
                session.commit()


def update_qr(dispatch_id,start_sn,end_sn,):
    with SessionContext() as session:
        session.execute(QRModel.__table__.update().where(QRModel.sn>=start_sn).where(QRModel.sn<=end_sn).values(dispatch_id=dispatch_id))
        session.commit()
