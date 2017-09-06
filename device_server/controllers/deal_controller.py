#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.01
交易单处理
"""

from super_models.deal_model import Deal
from super_models.database import Session
from super_models.store_model import Store
import hashlib
from log_util.device_logger import logger
from device_server.utils.comment import b64_aes_dec, aes_enc_b64
from device_server.response.res import success_response, succss_response_content,fail_response,fail_response_with_str,response
from device_server.response import errors
from redis_manager import redis_center,r_store_info
import json
from datetime import datetime
from reco.main.reco_main import RecoMain
from redis_manager import r_upload_token
import hashlib,os
import traceback,time,imp
from reco.main.reco_main_temp import RecoMain as TempRecoMain
import StringIO, gzip


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
            live['tax'] = total_price * 0.1

            channel = 'live_deal' + str(tcp_socket.store_id)

            redis_center.publish(channel, live)

        finally:
            session.close()
            tcp_socket.send(send)
            logger.info(send)


def save_order(order,device_sn,store_id):
    is_valid_order = order.get('is_valid_order')
    if not is_valid_order:
        return
    total_price = order.get('total')
    if not total_price:
        total_price=0
    itmes_list = order.get('items')
    if not itmes_list:
        itmes_list = []
    deal = Deal()
    deal.sn = order.get('sn')
    deal.time = order.get('time')
    deal.tax = order.get('tax')
    deal.orgin = order.get('txt_data')

    orgin_id = order.get('order_id')

    session = Session()

    if not orgin_id:
        return
    else:
        try:
            old_deal = session.query(Deal).filter_by(orgin_id=orgin_id).first()
        except Exception,e:
            logger.info(e)
        else:
            if old_deal:
                logger.info('same_order_id:{orgin_id}'.format(orgin_id = orgin_id))
                return
        finally:
            session.close()



    if not deal.time:
        deal.time = 0
    deal.datetime = datetime.fromtimestamp(int(int(deal.time) / 1000))

    deal.store_id = store_id
    store_name = r_store_info.get(str(store_id))
    if not store_name:
        store = session.query(Store).filter_by(store_id=store_id).first()
        if store:
            store_name = store.name
        else:
            store_name = ''

        r_store_info.set(str(store_id),store_name)

    deal.device_sn = device_sn
    deal.total_price = int(total_price)
    deal.items_list = json.dumps(itmes_list)
    deal.orgin_id = orgin_id

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
        live['tax'] = deal.tax

        channel = 'live_deal' + str(store_id)

        redis_center.publish(channel, live)
    finally:
        session.close()

def save_to_file(file_name, contents):
    contents = str(contents)
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
        send = fail_response_with_str(data,e.message)
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


def upload_orderhex(data,tcp_socket):
    # version = data.get('version')
    # if int(version) == 2:
    #     compress = data.get('content')
    #     content = gzdecode(compress)
    #     print compress
    #     print content
    # else:
    #     print version
    #
    # return

    content = data.get('content')
    try:
        _reco_main = TempRecoMain(content)
        result_dict = _reco_main.parse()
    except Exception,e:
        logger.error(e)
        save_to_file(tcp_socket.device_sn,content)
        logger.info(type(e.message))
        send = fail_response_with_str(data,'parse error')
        tcp_socket.send(send)
    else:
        if not result_dict:
            send = fail_response_with_str(data, 'no parse result')
            tcp_socket.send(send)
            return

        resp_list = []
        try:
            success = result_dict.get('status')
            order_list = result_dict.get('order_list')
            if not success:
                logger.info('convert result status not success')
                save_to_file(tcp_socket.device_sn, content)
                send = fail_response_with_str(data, 'Result status is False')
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
            logger.info('save order error')
            save_to_file(tcp_socket.device_sn, content)
            send = fail_response_with_str(data, e.message)
            tcp_socket.send(send)
        else:
            respon = success_response(data)
            tcp_socket.send(respon)

def gzdecode(data) :
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    result = gziper.read()   # 读取解压缩后数据
    return result

def pass_to_conversion(tcp_socket,data):
    compress = data.get('content')
    content = gzdecode(compress)


    superPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,os.pardir))
    folderPath = superPath + '/conversion_scripts/'
    script_name = '{device_sn}.py'.format(device_sn=tcp_socket.device_sn)
    scriptPath = folderPath + script_name

    # 判断是否存在脚本
    try:
        py_module = imp.load_source('module.name', scriptPath)
    except Exception,e:
        logger.error('no such convert script')
    else:
        try:
            result_dict = py_module.format_convert(content)
        except Exception,e:
            logger.info(e)
            logger.error('format_convert failed')
        else:
            if not result_dict:
                send = fail_response_with_str(data, 'no parse result')
                tcp_socket.send(send)
                return

            resp_list = []
            try:
                success = result_dict.get('status')
                order_list = result_dict.get('order_list')
                if not success:
                    logger.info('convert result status not success')
                    save_to_file(tcp_socket.device_sn, content)
                    send = fail_response_with_str(data, 'Result status is False')
                    tcp_socket.send(send)
                    return
                for result in order_list:
                    order = result.get('order')
                    if order:
                        save_order(order, tcp_socket.device_sn, tcp_socket.store_id)
                    result.pop('order')
                    resp_list.append(result)
            except Exception, e:
                logger.error(e)
                logger.info('save order error')
                save_to_file(tcp_socket.device_sn, content)
                send = fail_response_with_str(data, e.message)
                tcp_socket.send(send)
            else:
                respon = success_response(data)
                tcp_socket.send(respon)




# if __name__ == '__main__':
#     pass_to_conversion('600001','hello')