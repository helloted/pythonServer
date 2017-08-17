#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.04
用户账户网络请求
"""
from flask import Blueprint
from flask import request
from app_server.utils.request_handle import basic_unpack,login_required
from app_server.response import success_resp,failed_resp
from redis_manager import redis_center
from app_server.controllers.user_contrller import user_add
from app_server.models import SessionContext
from app_server.models.user_model import User
from app_server.controllers import user_contrller
import random,time
from log_util.app_logger import logger
from app_server.response.errors import *
from app_server.utils import db_error_record
from redis_manager import redis_center
from app_server.utils.imgtool import image_save
from app_server.models.favorite_model import FavoriteStore

user_token_key = 'app_user_token'

node_user=Blueprint('user_layer',__name__,)


@node_user.route('/register', methods=['POST'])
@basic_unpack
def user_register():
    body = request.json
    if not body:
        return failed_resp(ERROR_Parameters)
    else:
        code = body.get('code')
        password = body.get('password')
        phone = body.get('phone')

        if not phone and not password:
            return  failed_resp(ERROR_Parameters)

        store_code = redis_center.get(phone)

        if not store_code or not store_code == code:
            return failed_resp(ERROR_Verification_Code)

        with SessionContext(db_error_record) as session:
            user = session.query(User).filter_by(phone=phone).first()
            if user:
                return failed_resp(ERROR_Phone_Exists)

            user_add(phone, password)
            data = {}
            return success_resp(data)


@node_user.route('/password', methods=['POST'])
@basic_unpack
def user_password():
    body = request.json
    if not body:
        return failed_resp(ERROR_Parameters)
    else:
        code = body.get('code')
        password = body.get('password')
        phone = body.get('phone')

        if not phone and not password:
            return  failed_resp(ERROR_Parameters)

        store_code = redis_center.get(phone)

        if not store_code or not store_code == code:
            return failed_resp(ERROR_Verification_Code)
        with SessionContext(db_error_record) as session:
            user = session.query(User).filter_by(phone=phone).first()
            if user:
                user.password = password
                session.commit()
                data = {}
                return success_resp(data)
            else:
                return failed_resp(ERROR_User_Null)


@node_user.route('/login', methods=['POST'])
@basic_unpack
def user_login():
    body = request.json
    if not body:
        return failed_resp(ERROR_Parameters)
    else:
        password = body.get('password')
        phone = body.get('phone')
        with SessionContext() as session:
            user = session.query(User).filter_by(phone=phone).first()
            if user and user.password == password:
                current_time = int(time.time())
                user.last_login_time = current_time
                session.commit()

                token = user_contrller.product_token(phone)
                save_key = user_token_key + str(user.user_id)
                redis_center.set(save_key,token)
                data = {}
                data['token'] = token
                for key, value in vars(user).items():
                    if key == 'id' or key == '_sa_instance_state' or key == 'password':
                        continue
                    else:
                        data[key] = value

                count = session.query(FavoriteStore).filter_by(user_id=user.user_id).count()
                data['favorite_amount'] = count

                session.result =  success_resp(data)
            else:
                session.result =  failed_resp(ERROR_Login_Failed)
        return session.result


@node_user.route('/logout', methods=['GET'])
@basic_unpack
def user_logout():
    paras = request.args
    user_id = paras.get('user_id')
    key = user_token_key + user_id
    redis_center.delete(key)
    return success_resp()



@node_user.route('/code', methods=['GET'])
@basic_unpack
def get_code():
    paras = request.args

    phone = paras.get('phone')

    if phone:
        code = str(random.randint(100000, 999999))

        redis_center.set(phone,code)

        print phone

        data = {}
        data['code'] = code
        return success_resp(data)
    else:
        return failed_resp(ERROR_Parameters)



@node_user.route('/', methods=['GET'])
@basic_unpack
@login_required
def user():
    paras = request.args
    user_id = paras.get('user_id')
    with SessionContext() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            data= {}
            for key, value in vars(user).items():
                if key == 'id' or key == '_sa_instance_state' or key == 'password':
                    continue
                else:
                    data[key] = value
            return success_resp(data)
        else:
            return failed_resp(ERROR_User_Null)


@node_user.route('/update', methods=['POST'])
@basic_unpack
@login_required
def user_update():
    body = request.json
    if not body:
        return failed_resp(ERROR_Parameters)
    else:
        user_id = request.args.get('user_id')
        with SessionContext() as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            if user:
                if 'sex' in body:
                    user.sex = body['sex']

                if 'name' in body:
                    user.name = body['name']

                if 'birthday' in body:
                    user.birthday = body['birthday']

                if 'city' in body:
                    user.city = body['city']

                session.commit()

                data = {}
                return success_resp(data)
            else:
                return failed_resp(ERROR_User_Null)


@node_user.route('/icon', methods=['POST'])
@basic_unpack
@login_required
def user_icon():
    img = request.files['img']
    user_id = request.args.get('user_id')
    if not user_id:
        user_id = 0
    full_path =  image_save(user_id, img)
    with SessionContext() as session:
        user =  session.query(User).filter_by(user_id=user_id).first()
        user.icon = full_path
        session.commit()
        data = {}
        data['icon'] = full_path
        session.result = success_resp(data)
    return session.result

