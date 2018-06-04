#coding=utf-8
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Blueprint
from flask import request,make_response
from response import success_resp,failed_resp
from response import errors
from tools.request_handle import request_unpack,web_login_required,web_transfer
import time,json
from tools.comment import aes_enc_b64
from models.database import SessionContext
from models.agentModel import AgentModel
from models.applyModel import ApplyModel
from log_util.app_logger import logger
from redis_manager import redis_web_center
from flask import session as webSession
from models.product_info_model import ProductInfoModel
from models.dispatch_model import DispatchModel
from datetime import timedelta
from flask import app
import multiprocessing
from models.QRmodel import QRModel
import traceback


node_agent=Blueprint('agent_layer',__name__,)


@node_agent.route('/register', methods=['POST','OPTIONS'])
@web_transfer
def qr_scan(data):
    phone = data.get('phone')
    password = data.get('password')
    name = data.get('name')
    if phone and password:
        with SessionContext() as session:
            already = session.query(AgentModel).filter(AgentModel.phone==phone).first()
            if already:
                session.result = failed_resp(errors.ERROR_Phone_Exists)
            else:
                agent = AgentModel()
                agent.phone = phone
                agent.password = password
                agent.name = name
                session.add(agent)
                session.commit()
                session.result = success_resp()
        logger.info(session.result.log)
        return session.result.data
    else:
        return failed_resp(errors.ERROR_Parameters).data


@node_agent.route('/login', methods=['POST','OPTIONS'])
@web_transfer
def login(data):
    phone = data.get('phone')
    password = data.get('password')
    agent_id = 0
    if phone and password:
        with SessionContext() as session:
            mer = session.query(AgentModel).filter(AgentModel.phone==phone).first()
            if mer and mer.password == password:
                before = phone + '/' + str(int(time.time()))
                token = aes_enc_b64(before)
                agent_id = mer.id
                redis_web_center.set(name=agent_id,value=token)
                res_data = {'agent_id':agent_id,'level':mer.level}
                res_data['phone'] = mer.phone
                session.result = success_resp(res_data)
            else:
                session.result = failed_resp(errors.ERROR_Login_Failed)

        webSession.permanent = True
        webSession['agent_id'] = agent_id
        webSession['login_status'] = 'login'

        return session.result.data
    else:
        return failed_resp(errors.ERROR_Parameters).data


@node_agent.route('/list', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
def list_all():
    with SessionContext() as session:
        agents = session.query(AgentModel).all()
        data = []
        for mer in agents:
            a_dict = {}
            a_dict['agent_id'] = mer.id
            a_dict['agent_name'] = mer.name

            data.append(a_dict)

        session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data


@node_agent.route('/apply', methods=['POST','OPTIONS'])
@web_transfer
@web_login_required
def apply_code(data):
    agent_id = None
    if 'agent_id' in webSession:
        agent_id = webSession['agent_id']

    if not agent_id:
        return failed_resp(errors.ERROR_Login_First).data

    company = data.get('company')
    brand = data.get('brand')
    count = data.get('count')
    others = data.get('others')
    if not company or not brand or not count:
        res = failed_resp(errors.ERROR_Parameters)
        logger.info(res.log)
        return res.data

    with SessionContext() as session:
        apply_model = ApplyModel()
        apply_model.agent_id = int(agent_id)
        current = int(time.time())
        apply_model.apply_time = current
        sn = str(agent_id) + '_' + str(current)
        apply_model.apply_sn = sn
        apply_model.count = count
        apply_model.status = 1
        apply_model.company = company
        apply_model.brand = brand
        if others:
            apply_model.others = json.dumps(others)

        session.add(apply_model)
        session.commit()

        data = {'apply_sn':sn}

        session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data


@node_agent.route('/apply_list', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
def apply_list():
    agent_id = None
    if 'agent_id' in webSession:
        agent_id = webSession['agent_id']

    if not agent_id:
        return failed_resp(errors.ERROR_Login_First).data

    agent_id_int = int(agent_id)

    page = request.args.get('page')
    amount = request.args.get('amount')
    if not page or not amount:
        return failed_resp(errors.ERROR_Parameters).data
    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int-1) * amount_int
    with SessionContext() as session:
        res = session.query(ApplyModel).filter(ApplyModel.agent_id==agent_id_int).limit(amount_int).offset(offset).all()
        total = session.query(ApplyModel).filter(ApplyModel.agent_id==agent_id_int).count()
        total_num = total / amount_int + 1
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
            apply_list.append(dic)
        data = {}
        data['page_current'] = page_int
        data['page_count'] = total_num
        data['list'] = apply_list
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data



@node_agent.route('/set_list', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
def info_list():
    agent_id = None
    if 'agent_id' in webSession:
        agent_id = webSession['agent_id']

    if not agent_id:
        return failed_resp(errors.ERROR_Login_First).data

    agent_id_int = int(agent_id)

    info_list = []

    dispatch_id = request.args.get('dispatch_id')


    with SessionContext() as session:
        query = session.query(ProductInfoModel).filter(ProductInfoModel.agent_id==agent_id_int,ProductInfoModel.status==2)

        if dispatch_id:
            query = query.filter(ProductInfoModel.dispatch_id==int(dispatch_id))
        s_list = query.all()

        for info in s_list:
            i_dict = {}
            i_dict['company'] = info.company
            i_dict['brand'] = info.brand
            i_dict['start_sn'] = info.start_sn
            i_dict['end_sn'] = info.end_sn
            i_dict['agent_id'] = info.agent_id
            i_dict['product_id'] = info.id
            i_dict['dispatch_id'] = info.dispatch_id
            i_dict['time'] = info.time
            i_dict['count'] = info.count
            i_dict['status'] = info.status

            info_list.append(i_dict)

        session.result = success_resp(info_list)
    logger.info(session.result.log)
    return session.result.data


@node_agent.route('/set_info', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
def product_dispatch():
    agent_id = None
    if 'agent_id' in webSession:
        agent_id = webSession['agent_id']

    if not agent_id:
        return failed_resp(errors.ERROR_Login_First).data

    agent_id_int = int(agent_id)

    start_sn = request.args.get('start_sn')
    end_sn = request.args.get('end_sn')
    company = request.args.get('company')
    brand = request.args.get('brand')
    count = request.args.get('count')
    dispatch_id = request.args.get('dispatch_id')
    if not start_sn or not end_sn or not company or not brand or not count or not dispatch_id:
        return failed_resp(errors.ERROR_Parameters).data

    need_count = int(count)
    start_int = int(start_sn)
    end_int = int(end_sn)

    if start_int >= end_int:
        resp = failed_resp(errors.ERROR_Wrong_SN)
        logger.info(resp.log)
        return resp.data

    with SessionContext() as session:
        start_between = session.query(ProductInfoModel).filter(ProductInfoModel.status==2).filter((ProductInfoModel.start_sn <= start_int) & (ProductInfoModel.end_sn >= start_int)).first()
        end_between = session.query(ProductInfoModel).filter(ProductInfoModel.status==2).filter((ProductInfoModel.start_sn <= end_int) & (ProductInfoModel.end_sn >= end_int)).first()
        if start_between or end_between:
            session.result = failed_resp(errors.ERROR_Wrong_SN)
        else:
            product = ProductInfoModel()
            product.company = company
            product.brand = brand
            product.start_sn = start_sn
            product.end_sn = end_sn
            product.agent_id = agent_id_int
            product.dispatch_id = dispatch_id
            product.count = count
            product.time = int(time.time())
            product.status = 1

            session.add(product)
            session.commit()

            data = {}
            data['product_info_id'] = product.id

            # 新开进程去设置信息
            p = multiprocessing.Process(target=set_info, args=(start_int, need_count,product.id))
            p.start()

            session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data



@node_agent.route('/product_update', methods=['GET','OPTIONS'])
@web_transfer
@web_login_required
def product_update():
    product_id = request.args.get('product_id')
    status = request.args.get('status')

    if not product_id or not status:
        logger.info(failed_resp(errors.ERROR_Parameters).log)
        return failed_resp(errors.ERROR_Parameters).data

    with SessionContext() as session:
        product = session.query(ProductInfoModel).filter(ProductInfoModel.id==product_id).first()
        if product:
            product.status = status
            session.commit()
            session.result = success_resp()
        else:
            session.result = failed_resp(errors.ERROR_NO_Such_Values)

    logger.info(session.result.log)
    return session.result.data



def set_info(start_sn,count,product_info_id):
    with SessionContext() as session:
        try:
            # 批量执行
            inter = 100
            temp = 0
            for i in xrange(count):
                if temp < inter:
                    temp += 1
                else:
                    update_qr(product_info_id,start_sn,start_sn+temp-1)
                    start_sn = start_sn + temp
                    temp = 1
            update_qr(product_info_id, start_sn, start_sn + temp - 1)
        except Exception,e:
            logger.error(traceback.format_exc())
        else:
            logger.info('set info success product_info_id:{product_info_id}'.format(product_info_id=product_info_id))
            product = session.query(ProductInfoModel).filter(ProductInfoModel.id==product_info_id).first()
            if product:
                product.status = 2
                session.commit()


def update_qr(product_info_id,start_sn,end_sn):
    with SessionContext() as session:
        session.execute(QRModel.__table__.update().where(QRModel.sn>=start_sn).where(QRModel.sn<=end_sn).values(product_info_id=product_info_id))
        session.commit()




if __name__ == '__main__':
    set_info(100,2000,product_info_id=3)