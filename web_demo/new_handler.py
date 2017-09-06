#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.22
新增的几个接口
"""

import tornado.web
from super_models.store_model import Store
from super_models.deal_model import Deal
import json
from db_tool import SessionContext
import tornado.web
from super_models.deal_model import Deal
from super_models.store_model import Store
from super_models.database import Session
import json
from sqlalchemy import func
from log_util.web_demo_logger import logger
from sqlalchemy import extract
import datetime
from super_models.history_model import OfflineHistroy
from super_models.history_model import EventsHistroy


class AllStores(tornado.web.RequestHandler):
    def get(self):
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.add_header("Access-Control-Allow-Credentials", 'true')

        region_code = self.get_argument('region_code')
        district_list = []
        count = 0
        with SessionContext() as session:
            count = session.query(EventsHistroy).filter_by(status=0).count()
            results = session.query(Store.district).filter_by(region_code=region_code).group_by(Store.district).all()
            for i, val in enumerate(results):
                district = val[0]
                dis_dict = {}
                dis_dict['district'] = district
                store_list = []
                stores = session.query(Store).filter_by(district=district).all()
                for store in stores:
                    store_dict = {}
                    store_dict['store_id'] = store.store_id
                    store_dict['store_name'] = store.name
                    store_dict['store_sn'] = store.store_sn
                    store_list.append(store_dict)
                dis_dict['stores'] = store_list

                district_list.append(dis_dict)

        content = {}
        content['events'] = count
        content['results'] = district_list

        data = {}
        data['code'] = 0
        data['msg'] = 'success'
        data['data'] = content
        self.write(json.dumps(data))


class OfflineHistoryHandelr(tornado.web.RequestHandler):
    def get(self):
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.add_header("Access-Control-Allow-Credentials", 'true')

        result_list = []
        with SessionContext() as session:
            results = session.query(OfflineHistroy).all()
            for his in results:
                his_dict = {}
                his_dict['device_sn'] = his.device_sn
                his_dict['store_id'] = his.store_id
                his_dict['store_name'] = his.store_name
                his_dict['start'] = his.start_time
                his_dict['end_time'] = his.end_time

                result_list.append(his_dict)

        data = {}
        data['code'] = 0
        data['msg'] = 'success'
        data['data'] = result_list
        self.write(json.dumps(data))



if __name__ == '__main__':
    with SessionContext() as session:
        result = session.query(func.count('*'),func.sum(Deal.total_price),func.sum(Deal.tax)).all()
        print result


