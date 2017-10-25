#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.04
WEB服务器Layer处理
"""
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from flask import Blueprint
from flask import request
from super_models.device_model import Device
from web_server.models import SessionContext
from web_server.response.resp import add_headers,success_response,failed_response
import time,json,datetime
from super_models.deal_model import Deal


node_service=Blueprint('service_layer',__name__,)

@node_service.route('/dealID_scan', methods=['GET'])
@add_headers
def deal_ID():
    today = datetime.date.today()
    zero = str(today) + ' 00:00:00'
    st = time.strptime(zero, '%Y-%m-%d %H:%M:%S')
    yesterday_24_time = int(time.mktime(st)) * 1000
    yesterday_00_time = yesterday_24_time - 60 * 60 * 24 * 1000
    now = int(time.time()) * 1000
    with SessionContext() as session:
        yest_deals = session.query(Deal).filter(Deal.device_sn=='6201001000003',
                                           Deal.time.between(yesterday_00_time, yesterday_24_time)). \
            order_by((Deal.time).desc()).all()

        yest_str = '无记录'
        if len(yest_deals) > 0:
            
            yest_last = yest_deals[0]
            yest_str = yest_last.orgin_id


        deals = session.query(Deal).filter(Deal.device_sn=='6201001000003',
                                           Deal.time.between(yesterday_24_time, now)). \
            order_by((Deal.time)).all()

        count = len(deals)
        if count > 0:
            first_deal_id = deals[0].orgin_id
            last_deal_id = deals[count-1].orgin_id

            dif = int(last_deal_id[5:-3]) - int(first_deal_id[5:-3]) + 1

            if count == dif:
                result = '截止目前，6201001000003 今天总共交易了{count}单，昨天最后一单是{yest}，今天第一单单号是{first},最新一单单号是{last},今天单号是连续的'.format(count=count,first=first_deal_id,last=last_deal_id,yest=yest_str)
            else:
                sub = dif - count
                result = '截止目前，6201001000003 今天总共交易了{count}单，昨天最后一单是{yest}，今天第一单单号是{first},最新一单单号是{last},今天单号不连续，漏了{sub}单'.format(count=count,first=first_deal_id,last=last_deal_id,yest=yest_str,sub=sub)
        else:
            result = '今天还没开张呢，憋着急'
    return result





