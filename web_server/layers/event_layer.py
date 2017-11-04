#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.04
WEB服务器Layer处理
"""

from flask import Blueprint
from flask import request
from super_models.history_model import EventsHistroy
from web_server.models import SessionContext
from web_server.utils.handles import transfer
from web_server.utils.response import response_success,response_failed
from web_server.utils import errors
import time
from redis_manager import r_store_info
from super_models.store_model import Store
from log_util.web_demo_logger import logger


node_event=Blueprint('event_layer',__name__,)


@node_event.route('/', methods=['GET'])
@transfer
def event_list():
    page = request.args.get('page')
    amount = request.args.get('amount')

    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int - 1) * amount_int
    with SessionContext() as session:
        results = session.query(EventsHistroy).order_by((EventsHistroy.time.desc())).limit(amount_int).offset(offset).all()
        total = session.query(EventsHistroy).count()

        total_page = total / amount_int

        data = {}

        data['total_page'] = total_page
        data['current_page'] = page

        events = []
        for res in results:
            res_dict = {}
            res_dict['id'] = res.id
            res_dict['type'] = res.type
            res_dict['time'] = res.time
            res_dict['status'] = res.status
            store_id = res.store_id
            res_dict['store_id'] = store_id
            store_name = res.store_name
            if not store_name:
                store_name =  r_store_info.get(store_id)
                if not store_name:
                    store = session.query(Store).filter_by(store_id=store_id).first()
                    if store:
                        store_name = store.name
                        r_store_info.set(store_id,store_name)
            res_dict['store_name'] = store_name
            res_dict['level'] = 1

            if res.type == 1:
                device_sn = res.device_sn
                time_between = res.time_between

                x = time.localtime(res.start_time)
                start_time = time.strftime('%Y-%m-%d %H:%M:%S', x)

                y = time.localtime(res.end_time)
                end_time = time.strftime('%Y-%m-%d %H:%M:%S', y)

                res_dict['event'] = 'the device:' + str(device_sn) + ' lost connected' + ' from ' + str(start_time) + ' to ' + str(end_time)

            if res.type == 2:
                device_sn = res.device_sn

                x = time.localtime(res.start_time)
                start_time = time.strftime('%Y-%m-%d %H:%M:%S', x)

                res_dict['event'] = 'the port of device:' + str(device_sn) + ' lost connected' + ' at ' + str(start_time)
                res_dict['level'] = 2

            if res.type == 3:
                per_value = int(res.float_value * 100)
                res_dict['event'] = ' the total amount has changed: ' + str(res.value) + '  ' + str(per_value) + '%'

            events.append(res_dict)

        data['events'] = events
        session.result = response_success(data)
    logger.info(session.result.log)
    return session.result.resp_data


@node_event.route('/edit_status', methods=['POST'])
@transfer
def edit_status(post_body):
    event_id = post_body.get('id')
    status = post_body.get('status')
    with SessionContext() as session:
        event = session.query(EventsHistroy).filter_by(id=event_id).first()
        if event:
            event.status = status
            session.commit()
            session.result = response_success()
        else:
            session.result = response_failed(errors.ERROR_No_Such_Event)
    logger.info(session.result.log)
    return session.result.resp_data
