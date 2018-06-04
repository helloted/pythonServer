#coding=utf-8
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from flask import Blueprint
from flask import request,make_response,send_file
from flask import session as webSession
from response import success_resp,failed_resp
from response import errors
from tools.request_handle import manager_authorization_required,web_transfer,web_login_required
import time
from tools.comment import aes_enc_b64
from models.database import SessionContext
from models.agentModel import AgentModel
from log_util.app_logger import logger
from redis_manager import redis_center
from models.create_history_model import CreateHistoryModel
from models.QRmodel import QRModel
from sqlalchemy import func
from tools.generate import create_code
import multiprocessing
from models.applyModel import ApplyModel
import traceback


node_manager=Blueprint('manager_layer',__name__,)


@node_manager.route('/generate', methods=['POST','OPTIONS'])
@web_transfer
@web_login_required
@manager_authorization_required
def generate(data):
    count = data.get('count')
    with SessionContext() as session:
        last = session.query(func.max(QRModel.sn)).first()
        last_sn = last[0]
        start = last_sn + 1
        end = last_sn + count

        his = CreateHistoryModel()
        his.time = int(time.time())
        his.history_sn = his.time
        his.start_sn = start
        his.end_sn = end
        his.status = 1
        his.count = count

        session.add(his)
        session.commit()

        # 新开进程去生成二维码
        p = multiprocessing.Process(target=create_code, args=(start, count, his.history_sn))
        p.start()

        data = {'history_sn':his.history_sn}
        session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data


@node_manager.route('/generate_list', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
@manager_authorization_required
def history_list():
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not page or not amount:
        return failed_resp(errors.ERROR_Parameters)

    page_int = int(page)
    amount_int = int(amount)

    offset = (page_int-1) * amount_int

    with SessionContext() as session:
        res = session.query(CreateHistoryModel).limit(amount_int).offset(offset).all()
        total = session.query(CreateHistoryModel).count()
        total_num = total/amount_int + 1
        data = {}
        data['page_current'] = page_int
        data['page_count'] = total_num
        hist_list = []
        for his in res:
            dic = {}
            dic['time'] = his.time
            dic['history_sn'] = his.history_sn
            dic['start_sn'] = his.start_sn
            dic['end_sn'] = his.end_sn
            dic['status'] = his.status
            dic['count'] = his.count
            hist_list.append(dic)
        data['list'] = hist_list
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_manager.route('/hello', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
@manager_authorization_required
def hello():
    webSession['name'] = 'what'
    resp = make_response(success_resp().data)
    resp.set_cookie('token', '12345678')
    resp.set_cookie('agent_id', '12345678')
    return resp


@node_manager.route('/download', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
@manager_authorization_required
def download():
    his_sn = request.args.get('history_sn')
    if not his_sn:
        return failed_resp(errors.ERROR_Parameters).data

    superPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    folderPath = superPath + '/files/qrcode/'
    file_name = his_sn + '.txt'
    file_path = folderPath + file_name
    if os.path.exists(file_path):
        response = make_response(send_file(file_path))
        response.headers["Content-Disposition"] = "attachment; filename={filename};".format(filename=file_name)
        return response
    else:
        res = failed_resp(errors.ERROR_NO_Such_File)
        logger.info(res.log)
        return res.data


@node_manager.route('/delete', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
@manager_authorization_required
def delete_code():
    his_sn = request.args.get('history_sn')
    if not his_sn:
        res = failed_resp(errors.ERROR_Parameters)
        logger.info(res.log)
        return res.data
    else:
        with SessionContext() as session:
            his = session.query(CreateHistoryModel).filter(CreateHistoryModel.history_sn==his_sn).first()
            if his:
                session.delete(his)
                session.commit()
                session.result = success_resp()

                # 新开进程去生成二维码
                p = multiprocessing.Process(target=delete_qrcode, args=(his_sn,))
                p.start()
            else:
                session.result = failed_resp(errors.ERROR_NO_Such_Values)
        logger.info(session.result.log)
        return session.result.data


def delete_qrcode(history_sn):
    with SessionContext() as session:
        session.execute(QRModel.__table__.delete().where(QRModel.history_sn==history_sn))
        session.commit()
        print 'delete finish'


@node_manager.route('/apply_list', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
@manager_authorization_required
def apply_list():
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not page or not amount:
        return failed_resp(errors.ERROR_Parameters).data

    page_int = int(page)
    amount_int = int(amount)

    offset = (page_int-1) * amount_int

    with SessionContext() as session:
        res = session.query(ApplyModel).limit(amount_int).offset(offset).all()
        total = session.query(ApplyModel).count()
        total_num = total/amount_int + 1
        apply_list = []
        for apply in res:
            dic = {}
            dic['time'] = apply.apply_time
            dic['apply_sn'] = apply.apply_sn
            dic['start_sn'] = apply.start_sn
            dic['end_sn'] = apply.end_sn
            dic['status'] = apply.status
            dic['count'] = apply.count
            dic['company'] = apply.company
            dic['brand'] = apply.brand
            agent_id = apply.agent_id
            agent = session.query(AgentModel).filter(AgentModel.id==agent_id).first()
            if agent:
                dic['agent_name'] = agent.name

            apply_list.append(dic)
        data = {}
        data['page_current'] = page_int
        data['page_count'] = total_num
        data['list'] = apply_list
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_manager.route('/dispatch', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
@manager_authorization_required
def dispatch_code():
    apply_sn = request.args.get('apply_sn')
    status = request.args.get('status')
    if not apply_sn or not status:
        resp = failed_resp(errors.ERROR_Parameters)
        logger.info(resp.log)
        return resp.data
    status_num = int(status)
    with SessionContext() as session:
        apply = session.query(ApplyModel).filter(ApplyModel.apply_sn==apply_sn).first()
        if not apply:
            session.result = failed_resp(errors.ERROR_NO_Such_Values)
        else:
            # 分配二维码
            if status_num == 2:
                null_count = session.query(QRModel).filter(QRModel.apply_sn==None).count()
                need_count = apply.count

                # 剩余二维码不够
                if need_count > null_count:
                    session.result = failed_resp(errors.ERROR_NO_Enough_Code)
                else:
                    # 新开进程去生成二维码
                    p = multiprocessing.Process(target=dispath_qr, args=(apply_sn,need_count))
                    p.start()

                    session.result = success_resp()
            else: # 拒绝分配
                apply.status = status
                session.commit()
                session.result = success_resp()
    logger.info(session.result.log)
    return session.result.data


def dispath_qr(apply_sn,count):
    with SessionContext() as session:
        start_qr =  session.query(QRModel).filter(QRModel.apply_sn == None).order_by((QRModel.sn)).first()
        start_sn = start_qr.sn

        try:
            # 批量执行
            inter = 100
            temp = 0
            for i in xrange(count):
                if temp < inter:
                    temp += 1
                else:
                    update_qr(apply_sn,start_sn,start_sn+temp-1)
                    start_sn = start_sn + temp
                    temp = 1
            update_qr(apply_sn, start_sn, start_sn + temp - 1)
        except Exception,e:
            logger.error(traceback.format_exc())
        else:
            logger.info('dispatch success {sn}'.format(sn=apply_sn))
            apply = session.query(ApplyModel).filter(ApplyModel.apply_sn==apply_sn).first()
            if apply:
                apply.start_sn = start_qr.sn
                apply.end_sn = start_qr.sn + count -1
                apply.status = 2
                apply.dispatch_time = int(time.time())
                session.commit()


def update_qr(apply_sn,start_sn,end_sn,):
    print apply_sn,start_sn,end_sn
    with SessionContext() as session:
        session.execute(QRModel.__table__.update().where(QRModel.sn>=start_sn).where(QRModel.sn<=end_sn).values(apply_sn=apply_sn))
        session.commit()




