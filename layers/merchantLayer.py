import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from flask import Blueprint
from flask import request
from response import success_resp,failed_resp
from response import errors
from tools.request_handle import request_unpack
import time
from tools.comment import aes_enc_b64
from models.database import SessionContext
from models.merchantModel import MerchantModel
from log_util.app_logger import logger


node_merchant=Blueprint('merchant_layer',__name__,)

@node_merchant.route('/ver_code', methods=['GET'])
def ver_code():
    email = request.args.get('email')
    if email:
        return success_resp().data
    else:
        return failed_resp(errors.ERROR_Parameters).data


@node_merchant.route('/register', methods=['POST'])
@request_unpack
def qr_scan(data):
    # ver_code = data.get('ver_code')
    # if ver_code:
    #     logger.info(ver_code)
    # else:
    #     return failed_resp(errors.ERROR_Parameters).data

    phone = data.get('phone')
    name = data.get('name')
    brand = data.get('brand')
    password = data.get('password')

    with SessionContext() as session:
        mer = session.query(MerchantModel).filter(MerchantModel.phone == phone).first()
        if mer:
            resp = failed_resp(errors.ERROR_Phone_Exists)
            logger.info(resp.log)
            return resp.data

    if phone and name and brand and password:
        with SessionContext() as session:
            mer = MerchantModel()
            mer.phone = phone
            mer.brand = brand
            mer.password = password
            mer.name = name
            session.add(mer)
            session.commit()
            session.result = success_resp()
        logger.info(session.result.log)
        return session.result.data
    else:
        logger.info()
        return failed_resp(errors.ERROR_Parameters).data


@node_merchant.route('/modify', methods=['POST'])
@request_unpack
def modidy(data):
    # ver_code = data.get('ver_code')
    # if ver_code:
    #     logger.info(ver_code)
    # else:
    #     return failed_resp(errors.ERROR_Parameters).data

    user_id = request.args.get('user_id')

    name = data.get('name')
    brand = data.get('brand')
    password = data.get('password')

    with SessionContext() as session:
        mer = session.query(MerchantModel).filter(MerchantModel.id == user_id).first()
        if mer:
            if brand:
                mer.brand = brand
            if password:
                mer.password = password
            if name:
                mer.name = name
            session.commit()
            session.result = success_resp()
        else:
            session.result = failed_resp(errors.ERROR_NO_Such_Values)
    return session.result.data



@node_merchant.route('/login', methods=['POST'])
@request_unpack
def login(data):
    phone = data.get('phone')
    password = data.get('password')
    if phone and password:
        with SessionContext() as session:
            mer = session.query(MerchantModel).filter(MerchantModel.phone==phone).first()
            if mer and mer.password == password:
                before = str(mer.id) + '/' + str(int(time.time()))
                res_data = {'token':aes_enc_b64(before),'user_id':mer.id}
                res_data['phone'] = mer.phone
                res_data['email'] = mer.email
                res_data['brand'] = mer.brand
                res_data['name'] = mer.name
                session.result = success_resp(res_data)
            else:
                session.result = failed_resp(errors.ERROR_Login_Failed)
        logger.info(session.result.log)
        return session.result.data
    else:
        return failed_resp(errors.ERROR_Parameters).data







