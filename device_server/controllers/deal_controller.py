#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.01
交易单处理
"""

from super_models.deal_model import Deal
from super_models.database import Session
from super_models.device_store_model import DeviceStore
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
import StringIO, gzip,zlib
from gevent import monkey; monkey.patch_all()
import gevent
from super_models.deal_status_model import DealStatus
from celery import Celery

broker_url = 'redis://localhost:6379/10'
backend_url = 'redis://localhost:6379/11'

client = Celery('convert_deal', backend=backend_url, broker=broker_url)

def upload_deal(data,tcp_socket):
    device_sn = tcp_socket.device_sn
    try:
        content = data.get('content')
        deal_sn = content.get('deal_sn')
        deal_time = content.get('deal_time')
        content_json = json.dumps(content)
    except Exception,e:
        logger.error(e)
        send = fail_response(tcp_socket.device_sn, data, errors.ERROR_Deal_Received_Failed)
    else:
        if not deal_sn:
            logger.error('deal_sn is null')
            send = fail_response(tcp_socket.device_sn, data, errors.ERROR_Deal_Received_Failed)
        else:
            save_event = gevent.spawn(save_origin_file_to_folder,device_sn,deal_sn,deal_time,content_json)
            update_event = gevent.spawn(update_deal_record,device_sn,deal_sn)
            gevent.joinall([save_event,update_event])

            if save_event.value and update_event.value == 1:
                send = success_response(device_sn,data)
                try:
                    # 将订单送入消息通道
                    send_deal_to_celery(device_sn, deal_sn, content_json)
                except Exception,e:
                    logger.error(e)
                else:
                    logger.info('{deal_sn} deal received, saved, sent to convert success'.format(deal_sn=deal_sn))
            else:
                send = fail_response(device_sn, data, errors.ERROR_Deal_Received_Failed)
                logger.info('received deal {deal_sn} failed, save {save}, create {create}'.format(deal_sn=deal_sn,save=save_event.value,create=update_event.value))

    # 回复客户端上传订单情况
    try:
        tcp_socket.send(send.data)
    except Exception, e:
        logger.error(e)
    else:
        logger.info(send.log)


def save_origin_file_to_folder(device_sn,deal_sn,deal_time,content_json):
    super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))

    deal_sec = int(int(deal_time)/1000)
    date_str = time.strftime("%Y%m%d", time.localtime(deal_sec))

    # /files/original/6201001000100/20171023/
    folder_path = super_path + '/files/original/'+ device_sn + '/' + date_str
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    #  62010010001003r3fe3d.txt
    file_path = folder_path + '/' + deal_sn +'.txt'

    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.info('repeated deal_sn {deal_sn},remove old file'.format(deal_sn=deal_sn))

    try:
        fh = open(file_path, 'w')
        fh.write(content_json)
        fh.close()
    except Exception,e:
        logger.error(e)
        return False
    else:
        logger.info('original file saved:' + file_path)
        return True


def update_deal_record(device_sn, deal_sn):
    session = Session()
    try:
        deal_status = session.query(DealStatus).filter(DealStatus.deal_sn==deal_sn).first()
    except Exception,e:
        logger.error(e)
        return 0
    else:
        if not deal_status:
            deal_status = DealStatus()
            session.add(deal_status)
        else:
            logger.info('repeated deal_sn {deal_sn}'.format(deal_sn=deal_sn))

        now_msec = int(round(time.time() * 1000))
        deal_status.deal_sn = deal_sn
        deal_status.device_sn = device_sn
        deal_status.receive_time = now_msec
        deal_status.status = 0  # 已接收,但未解析

        try:
            session.commit()
        except Exception, e:
            logger.error(e)
            return 0 # 建档失败，需要重新上传
        else:
            return 1 # 建档成功
    finally:
        session.close()


def send_deal_to_celery(device_sn,deal_sn,content):
    msg_data = {}
    msg_data['device_sn'] = device_sn
    msg_data['deal_sn'] = deal_sn
    msg_data['content'] = content
    msg_json = json.dumps(msg_data)
    client.send_task('convert_center.receive', (msg_json,))


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
    #     send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Upload_Token_Incorrect)
    #     tcp_socket.send(send)
    #     return

    try:
        _reco_main = RecoMain(content.get('capture_data'))
        result_dict = _reco_main.parse()
    except Exception,e:
        logger.error(e)
        save_to_file(tcp_socket.device_sn,content_str)
        send = fail_response(tcp_socket.device_sn,data,errors.ERROR_Deal_Para_Error)
        try:
            tcp_socket.send(send.data)
        except Exception, e:
            logger.error(e)
        else:
            logger.info(send.log)
    else:
        resp_list = []
        try:
            success = result_dict.get('status')
            order_list = result_dict.get('order_list')
            if not success:
                save_to_file(tcp_socket.device_sn, content_str)
                send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Deal_Para_Error)
                try:
                    tcp_socket.send(send.data)
                except Exception, e:
                    logger.error(e)
                else:
                    logger.info(send.log)
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
            send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Deal_Para_Error)
            try:
                tcp_socket.send(send.data)
            except Exception, e:
                logger.error(e)
            else:
                logger.info(send.log)
        else:
            orgin_data = {}
            orgin_data['orders'] = order_list
            send = response(tcp_socket.device_sn,data,orgin_data)
            try:
                tcp_socket.send(send.data)
            except Exception, e:
                logger.error(e)
            else:
                logger.info(send.log)


def gzdecode(data) :
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    result = gziper.read()   # 读取解压缩后数据
    return result


def save_origin_deal_to_folder(device_sn,deal_sn, contents):
    contents = str(contents)
    super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
    full_time_str = datetime.now().strftime('%H_%M_%S')

    date_str = datetime.now().strftime('%Y%m%d')

    # /files/original/6201001000100/20171023/
    folder_path = super_path + '/files/original/'+ device_sn + '/' + date_str
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    #  62010010001003r3fefe_15_28_35
    file_path = folder_path + '/' + deal_sn  +'_'+ full_time_str +'.txt'
    try:
        fh = open(file_path, 'w')
        fh.write(contents)
        fh.close()
    except Exception,e:
        logger.error(e)
        return False
    else:
        logger.info('orginal file saved:' + file_path)
        return True


def upload_orderhex(data,tcp_socket):
    version = data.get('version')
    version = int(version)
    if version == 1:
        logger.error('the version is 1')
    else:
        pass_to_conversion(data,tcp_socket)


def save_all_deal_to_folder(device_sn, contents):
    contents = str(contents)
    super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))


    full_time_str = datetime.now().strftime('%H_%M_%S_%f')

    date_str = datetime.now().strftime('%Y%m%d')

    folder_path = super_path + '/files/original/'+ device_sn + '/' + date_str
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = folder_path + '/' + device_sn  +'_'+ full_time_str +'.txt'
    logger.info('orginal file saved:'+file_path)
    fh = open(file_path, 'w')
    fh.write(contents)
    fh.close()

def pass_to_conversion(data,tcp_socket):
    content = data.get('content')
    save_all_deal_to_folder(tcp_socket.device_sn,content)
    superPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,os.pardir))
    folderPath = superPath + '/conversion_scripts/'
    script_name = 's_{device_sn}.py'.format(device_sn=tcp_socket.device_sn)
    scriptPath = folderPath + script_name

    # 判断是否存在脚本
    try:
        py_module = imp.load_source('s_{device_sn}'.format(device_sn=tcp_socket.device_sn), scriptPath)
    except Exception,e:
        logger.error(e)
        logger.error('{device} load script error'.format(device=tcp_socket.device_sn))
        send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Deal_Para_Error)
        save_to_file(tcp_socket.device_sn, content)
        try:
            tcp_socket.send(send.data)
        except Exception, e:
            logger.error(e)
        else:
            logger.info(send.log)
    else:
        try:
            result_dict = py_module.format_convert(content)
        except Exception,e:
            logger.error(traceback.format_exc())
            logger.info('format_convert failed')
            send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Deal_Para_Error)
            save_to_file(tcp_socket.device_sn, content)
            try:
                tcp_socket.send(send.data)
            except Exception, e:
                logger.error(e)
            else:
                logger.info(send.log)
        else:
            if not result_dict:
                logger.error('not success para')
                send = fail_response(tcp_socket.device_sn,data,errors.ERROR_Deal_Para_Error)
                try:
                    tcp_socket.send(send.data)
                except Exception, e:
                    logger.error(e)
                else:
                    logger.info(send.log)
                return

            logger.info(result_dict)
            success = result_dict.get('status')
            order_type = result_dict.get('orderType')

            if success and order_type == 1:
                try:
                    save_order(result_dict, tcp_socket.device_sn, tcp_socket.store_id)
                except Exception, e:
                    logger.error(e)
                    logger.info('save order error')
                    save_to_file(tcp_socket.device_sn, content)
                    send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Deal_Para_Error)
                    try:
                        tcp_socket.send(send.data)
                    except Exception, e:
                        logger.error(e)
                    else:
                        logger.info(send.log)
                else:
                    result_dict.pop('orgin')
                    orgin_data = {}
                    orgin_data['order'] = result_dict
                    send = response(tcp_socket.device_sn,data, orgin_data)
                    try:
                        tcp_socket.send(send.data)
                    except Exception, e:
                        logger.error(e)
                    else:
                        logger.info(send.log)
            else:
                # 存到失败文件夹
                if not success and order_type == 1:
                    save_to_file(tcp_socket.device_sn, content)
                elif order_type == 0:
                    save_to_file(tcp_socket.device_sn, content)

                # 回复设备端
                send = fail_response(tcp_socket.device_sn,data, errors.ERROR_Deal_Para_Error)
                try:
                    tcp_socket.send(send.data)
                except Exception, e:
                    logger.error(e)
                else:
                    logger.info(send.log)


def save_order(order, device_sn, store_id):
    deal = Deal()
    deal.sn = order.get('sn')
    deal.time = order.get('time')
    deal.tax = order.get('tax')
    deal.orgin = order.get('orgin')

    orgin_id = order.get('order_id')

    session = Session()

    if not orgin_id:
        return
    else:
        try:
            old_deal = session.query(Deal).filter_by(orgin_id=orgin_id).first()
        except Exception, e:
            logger.error(e)
        else:
            if old_deal:
                logger.info('same_order_id:{orgin_id}'.format(orgin_id=orgin_id))
                return
        finally:
            session.close()

    store_session = Session()
    if not deal.time:
        deal.time = 0
    deal.datetime = datetime.fromtimestamp(int(int(deal.time) / 1000))

    deal.store_id = store_id


    total_price = order.get('total_price')
    if not total_price:
        total_price = 0
    itmes_list = order.get('items_list')
    if not itmes_list:
        itmes_list = []
    deal.device_sn = device_sn
    deal.total_price = int(total_price)
    deal.items_list = json.dumps(itmes_list)
    deal.orgin_id = orgin_id

    new_session = Session()
    new_session.add(deal)

    try:
        new_session.commit()
    except Exception, e:
        new_session.rollback()
        logger.error(e.message)
    else:
        logger.debug('save order{sn} success'.format(sn=order.get('sn')))
        
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
        new_session.close()

# if __name__ == '__main__':
#     timestamp = 1510217234828
#     deal_sec = int(int(timestamp)/1000)
#     date_str = time.strftime("%Y%m%d", time.localtime(deal_sec))
#     print date_str