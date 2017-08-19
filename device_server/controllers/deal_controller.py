#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.01
交易单处理
"""

from super_models.deal_model import Deal
from super_models.database import Session
import hashlib
from log_util.device_logger import logger
from device_server.utils.comment import b64_aes_dec, aes_enc_b64
from device_server.response.res import success_response, succss_response_content,fail_response,fail_response_with_str,response
from device_server.response import errors
from redis_manager import redis_center
import json
from datetime import datetime
from reco.main.reco_main import RecoMain
from redis_manager import r_upload_token
import hashlib,os
import traceback,time


def verify_sn(deal_sn,time,device_sn,seed_token):
    timestr = str(time)

    text = device_sn + seed_token + timestr
    base = aes_enc_b64(text)
    hah = hashlib.sha1(base).hexdigest()

    logger.info('text'+text)
    logger.info('hash'+hah)
    logger.info(deal_sn)

    verify = hah[:6]

    post_verify = deal_sn[-6:]

    if post_verify == verify:
        return True
    else:
        logger.error('post_verify:{post},myverify:{my}'.format(post=post_verify,my=verify))
        return False


def upload_deal(data,tcp_socket):
    seq = data.get('seq')
    content = data.get('content')

    deal_sn = content.get('deal_sn')
    deal_time = content.get('deal_time')
    device_sn = content.get('device_sn')

    seedtoken = 'seed'

    verify = verify_sn(deal_sn,deal_time,device_sn,seedtoken)

    #交易序列号未通过验证
    if verify == False:
        send = fail_response(data,errors.ERROR_Deal_SN_NotVerify)
        tcp_socket.send(send)
    else:
        total_price = content.get('total_price')
        itmes_list = content.get('list')
        deal = Deal()
        deal.sn = deal_sn
        deal.time = deal_time

        deal.datetime = datetime.fromtimestamp(int(deal_time/1000))

        deal.device_sn= tcp_socket.device_sn
        deal.store_id = tcp_socket.store_id
        deal.total_price = int(total_price)
        deal.items_list = json.dumps(itmes_list)

        session = Session()
        session.add(deal)


        try:
            session.commit()
        except Exception, e:
            session.rollback()
            send = fail_response(data,errors.ERROR_DataBase)
            logger.error(e.message)
        else:
            send = success_response(data)
            # 发送广播
            live = {}
            live['store_id'] = tcp_socket.store_id
            live['device_sn'] = tcp_socket.device_sn
            live['deal_sn'] = deal_sn
            live['time'] = deal_time
            live['total_price'] = total_price

            channel = 'live_deal' + str(tcp_socket.store_id)

            redis_center.publish(channel, live)

        finally:
            session.close()
            tcp_socket.send(send)
            logger.info(send)


def save_order(order,device_sn,store_id):
    total_price = order.get('total')
    if not total_price:
        total_price=0
    itmes_list = order.get('items')
    if not itmes_list:
        itmes_list = []
    deal = Deal()
    deal.sn = order.get('sn')
    deal.time = order.get('time')
    if not deal.time:
        deal.time = 0
    deal.datetime = datetime.fromtimestamp(int(int(deal.time) / 1000))

    deal.device_sn = device_sn
    deal.store_id = store_id
    deal.total_price = int(total_price)
    deal.items_list = json.dumps(itmes_list)

    session = Session()
    session.add(deal)

    try:
        session.commit()
    except Exception, e:
        session.rollback()
        logger.error(e.message)
    else:
        # 发送广播
        live = {}
        live['store_id'] = store_id
        live['device_sn'] = device_sn
        live['deal_sn'] = deal.sn
        live['time'] = deal.time
        live['total_price'] = total_price

        channel = 'live_deal' + str(store_id)

        redis_center.publish(channel, live)
    finally:
        session.close()

def save_to_file(file_name, contents):
    super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))

    time_now = int(time.time())
    time_local = time.localtime(time_now)
    full_date_str =  time.strftime("%H_%M_%S", time_local)

    date_str = time.strftime("%Y%m%d", time_local)

    folder_path = super_path + '/files/failed_capture/'+ date_str
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = folder_path + '/' + file_name  +'_'+ full_date_str +'.txt'
    logger.info('failed_save:'+file_path)
    fh = open(file_path, 'w')
    fh.write(contents)
    fh.close()


def upload_capture(data,tcp_socket):
    content_str = data.get('content')
    content = eval(content_str)
    token = content.get('upload_token')
    store_token = r_upload_token.get(tcp_socket.device_sn)
    # if not store_token:
    #     store_token = hashlib.md5(tcp_socket.device_sn +'qotaku_key').hexdigest()
    #     r_upload_token.set(tcp_socket.device_sn,store_token)
    #
    # if not token or not store_token == token:
    #     logger.info(('upload_token:',token,store_token))
    #     send = fail_response(data, errors.ERROR_Upload_Token_Incorrect)
    #     tcp_socket.send(send)
    #     return

    try:
        _reco_main = RecoMain(content.get('capture_data'))
        result_dict = _reco_main.parse()
    except Exception,e:
        logger.error(e)
        save_to_file(tcp_socket.device_sn,content_str)
        send = fail_response_with_str(data,traceback.format_exc())
        tcp_socket.send(send)
    else:
        resp_list = []
        try:
            success = result_dict.get('status')
            order_list = result_dict.get('order_list')
            if not success:
                save_to_file(tcp_socket.device_sn, content_str)
                send = fail_response_with_str(data, 'para failed')
                tcp_socket.send(send)
                return
            for result in order_list:
                order = result.get('order')
                if order:
                    save_order(order,tcp_socket.device_sn,tcp_socket.store_id)
                result.pop('order')
                resp_list.append(result)
        except Exception,e:
            logger.error(e)
            save_to_file(tcp_socket.device_sn, content_str)
            send = fail_response_with_str(data,e.message)
            tcp_socket.send(send)
        else:
            orgin_data = {}
            orgin_data['orders'] = order_list
            send = response(data,orgin_data)
            tcp_socket.send(send)



