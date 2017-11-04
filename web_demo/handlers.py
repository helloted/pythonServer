#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.12
店铺经营状况的一些接口
"""

import tornado.web
from super_models.deal_model import Deal
from super_models.store_model import Store
from super_models.database import Session
import json
from sqlalchemy import func
from log_util.web_demo_logger import logger
from sqlalchemy import extract
import datetime


class HistoryDevicesHandler(tornado.web.RequestHandler):
    def get(self):
        # devices = self.get_argument('devices')

        request_type = 0
        store_id = 1
        devices = self.get_argument('devices','no')
        if devices != 'no':
            request_type = 1
        else:
            store_id = self.get_argument('store_id', 1)
            request_type = 2


        start_time = int(self.get_argument('start_time'))
        end_time = int(self.get_argument('end_time'))

        devices_list = eval(devices)

        indexstr = self.get_argument('index')
        amount = int(self.get_argument('amount'))

        index = int(indexstr) - 1
        start = index * amount

        session = Session()
        try:
            if request_type == 1:
                deals = session.query(Deal).filter(Deal.device_sn.in_(devices_list),Deal.time.between(start_time, end_time)).\
                    order_by((Deal.time.desc())).limit(amount).offset(start).all()
                count = session.query(Deal).filter(Deal.device_sn.in_(devices_list),Deal.time.between(start_time, end_time)).count()
            else:
                deals = session.query(Deal).filter(Deal.store_id==store_id,Deal.time.between(start_time, end_time)).\
                    order_by((Deal.time.desc())).limit(amount).offset(start).all()
                count = session.query(Deal).filter(Deal.store_id==store_id,Deal.time.between(start_time, end_time)).count()
        except Exception,e:
            session.rollback()
            logger.info(e)
            resdic = {}
            resdic['code'] = 102
            resdic['message'] = 'history failed'
            resdic['data'] = None
        else:
            list = []
            for obj in deals:
                deal = {}
                deal['device_sn'] = obj.device_sn
                deal['deal_sn'] = obj.sn
                if obj.orgin_id:
                    deal['orgin_id'] = obj.orgin_id
                else:
                    deal['orgin_id'] = obj.sn
                deal['time'] = obj.time
                deal['total_price'] = obj.total_price
                deal['tax'] = obj.tax
                list.append(deal)

            data= {}
            data['index'] = indexstr
            data['amount'] = amount
            data['deals'] = list

            total_page = count/amount + 1

            data['total_page'] = total_page

            resdic = {}

            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data
        finally:
            session.close()

            jsonrsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(jsonrsp)

class HistoryStoreHandler(tornado.web.RequestHandler):
    def get(self):
        store_id = self.get_argument('store_id')

        indexstr = self.get_argument('index')
        amount = int(self.get_argument('amount'))

        start_time = int(self.get_argument('start_time'))
        end_time = int(self.get_argument('end_time'))

        index = int(indexstr) - 1
        start = index * amount

        session = Session()
        try:
            deals = session.query(Deal).filter(Deal.store_id == store_id,Deal.time.between(start_time, end_time)).\
                order_by((Deal.time.desc())).limit(amount).offset(start).all()
            count = session.query(Deal).filter(Deal.store_id == store_id,Deal.time.between(start_time, end_time)).count()
            store = session.query(Store).filter(Store.store_id==store_id).first()
        except Exception,e:
            session.rollback()
            print e
            resdic = {}
            resdic['code'] = 101
            resdic['message'] = 'history failed'
            resdic['data'] = None
        else:
            print 'count:',count
            list = []
            for obj in deals:
                deal = {}
                deal['device_sn'] = obj.device_sn
                deal['deal_sn'] = obj.sn
                orgin_id = store.name + '_'
                if obj.orgin_id:
                    orgin_id = orgin_id + obj.orgin_id
                else:
                    orgin_id = orgin_id + obj.sn
                deal['orgin_id'] = orgin_id
                deal['time'] = obj.time
                deal['total_price'] = obj.total_price
                deal['tax'] = obj.tax
                list.append(deal)


            data= {}
            data['index'] = indexstr
            data['amount'] = amount
            data['deals'] = list

            total_page = count/amount + 1

            data['total_page'] = total_page

            resdic = {}

            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data
        finally:
            session.close()

            jsonrsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(jsonrsp)


class HistoryDistrictHandler(tornado.web.RequestHandler):
    def get(self):
        district = self.get_argument('district')


        indexstr = self.get_argument('index')
        amount = int(self.get_argument('amount'))

        start_time = int(self.get_argument('start_time'))
        end_time = int(self.get_argument('end_time'))

        index = int(indexstr) - 1
        start = index * amount

        session = Session()
        try:
            deals = session.query(Deal).filter(Deal.store_id == Store.store_id,Store.district==district,Deal.time.between(start_time, end_time)).\
                order_by((Deal.time.desc())).limit(amount).offset(start).all()
            count = session.query(Deal).filter(Deal.store_id == Store.store_id,Store.district==district,Deal.time.between(start_time, end_time)).count()
        except Exception,e:
            session.rollback()
            print e
            resdic = {}
            resdic['code'] = 101
            resdic['message'] = 'history failed'
            resdic['data'] = None
        else:
            print 'count:',count
            list = []
            for obj in deals:
                deal = {}
                deal['device_sn'] = obj.device_sn
                deal['deal_sn'] = obj.sn
                deal['time'] = obj.time
                deal['total_price'] = obj.total_price
                deal['tax'] = obj.tax
                orgin_id = ''
                store = session.query(Store).filter(Store.store_id == obj.store_id).first()
                if store:
                    orgin_id = store.name + '_'
                if obj.orgin_id:
                    orgin_id = orgin_id + obj.orgin_id
                else:
                    orgin_id = orgin_id + obj.sn
                deal['orgin_id'] = orgin_id
                list.append(deal)


            data= {}
            data['index'] = indexstr
            data['amount'] = amount
            data['deals'] = list

            total_page = count/amount + 1

            data['total_page'] = total_page

            resdic = {}

            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data
        finally:
            session.close()

            jsonrsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(jsonrsp)



class DealDetailHandler(tornado.web.RequestHandler):
    def get(self):
        deal_sn = self.get_argument('deal_sn')

        session = Session()
        resdic = {}
        try:
            deal = session.query(Deal).filter_by(sn=deal_sn).first()
            store = session.query(Store).filter(Store.store_id == deal.store_id).first()
        except Exception,e:
            session.rollback()
            print e

            resdic['code'] = 101
            resdic['message'] = 'detail failed'
            resdic['data'] = None
        else:
            data= {}
            data['deal_id'] = deal.id
            orgin_id = ''
            if store:
                orgin_id = store.name + '_'
            if deal.orgin_id:
                orgin_id = orgin_id + deal.orgin_id
            else:
                orgin_id = orgin_id + deal.sn
            data['orgin_id'] = orgin_id
            data['orgin'] = deal.orgin
            data['deal_sn'] = deal.sn
            data['time'] = deal.time
            data['total_price'] = deal.total_price
            data['tax'] = deal.tax
            data['items'] = deal.items_list

            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data
        finally:
            session.close()

            jsonrsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(jsonrsp)



def get_days(begin_time,end_time):
    date_list = []
    begin_date = datetime.datetime.fromtimestamp(begin_time)
    end_date = datetime.datetime.fromtimestamp(end_time)
    while begin_date <= end_date:
        date_str = begin_date.strftime('%Y-%m-%d')
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list



class StatisticsDeviceHandler(tornado.web.RequestHandler):
    def get(self):
        devices = self.get_argument('devices')

        devices_list = eval(devices)

        start_time = int(self.get_argument('start_time'))
        end_time = int(self.get_argument('end_time'))
        session = Session()
        resdic = {}
        try:
            result = session.query(func.date_format(Deal.datetime, '%Y-%m-%d'), \
                                   func.count('*'),
                                   func.sum(Deal.total_price)).\
                             filter(Deal.time.between(start_time, end_time), \
                                          Deal.device_sn.in_(devices_list)).\
                             group_by(func.date_format(Deal.datetime, '%Y-%m-%d')).all()
            amount_result = session.query(
                                   func.count('*'),
                                   func.sum(Deal.total_price),
                                   func.sum(Deal.total_price)).\
                             filter(Deal.time.between(start_time, end_time), \
                                          Deal.device_sn.in_(devices_list)).all()
        except Exception,e:
            session.rollback()

            logger.error(e.message)

            resdic['code'] = 101
            resdic['message'] = 'statics failed'
            resdic['data'] = None
        else:
            dates = []
            counts = []
            totals = []

            days = get_days(int(start_time/1000),int(end_time/1000))

            for day in days:
                dates.append(day)
                index = -1
                for i, row in enumerate(result):
                    if str(row[0]) == day:
                        index = i

                if index == -1:
                    counts.append(0)
                    totals.append(0)
                else:
                    temp = result[index]

                    counts.append(temp[1])
                    totals.append(int(temp[2]))

            data = {}
            data['dates'] = dates
            data['counts'] = counts
            data['totals'] = totals

            data['tax_total'] = 0
            data['count_total'] = 0
            data['total_total'] = 0

            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data

        finally:
            session.close()
            json_rsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(json_rsp)



def get_months(begin_time,end_time):
    date_list = []
    begin_date = datetime.datetime.fromtimestamp(begin_time)
    end_date = datetime.datetime.fromtimestamp(end_time)
    while begin_date <= end_date:
        date_str = begin_date.strftime('%Y-%m')
        date_list.append(date_str)
        begin_date = add_months(begin_date, 1)
    return date_list

import calendar

def add_months(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


class StatisticsYearHandler(tornado.web.RequestHandler):
    def get(self):
        start_time = int(self.get_argument('start_time'))
        end_time = int(self.get_argument('end_time'))
        request_type = 0
        store_id = 1
        district = ''
        devices = self.get_argument('devices','no')
        if devices != 'no':
            request_type = 1
        else:
            store_id = self.get_argument('store_id', 0)
            if store_id != 0:
                request_type = 2
            else:
                district = self.get_argument('district', '')
                request_type = 3
        logger.info(district)
        session = Session()
        resdic = {}
        try:
            if request_type == 1:
                devices_list = eval(devices)
                result = session.query(func.date_format(Deal.datetime, '%Y-%m'), \
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)).\
                                 filter(Deal.time.between(start_time, end_time), \
                                            Deal.device_sn.in_(devices_list)).\
                                 group_by(func.date_format(Deal.datetime, '%Y-%m')).all()

                amount_result = session.query(
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)).\
                                 filter(Deal.time.between(start_time, end_time), \
                                              Deal.device_sn.in_(devices_list)).all()
            elif request_type == 2:
                result = session.query(func.date_format(Deal.datetime, '%Y-%m'), \
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), \
                           Deal.store_id==store_id). \
                    group_by(func.date_format(Deal.datetime, '%Y-%m')).all()

                amount_result = session.query(
                    func.count('*'),
                    func.sum(Deal.total_price),
                    func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), Deal.store_id == store_id).all()
            elif request_type == 3:
                logger.info('======================')
                logger.info(district)
                result = session.query(func.date_format(Deal.datetime, '%Y-%m'), \
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), \
                           Deal.store_id == Store.store_id, Store.district == district). \
                    group_by(func.date_format(Deal.datetime, '%Y-%m')).all()

                amount_result = session.query(
                    func.count('*'),
                    func.sum(Deal.total_price),
                    func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), Deal.store_id == Store.store_id, Store.district == district).all()

        except Exception,e:
            session.rollback()

            logger.error(e.message)

            resdic['code'] = 101
            resdic['message'] = 'statics failed'
            resdic['data'] = None
        else:
            dates = []
            counts = []
            totals = []
            taxs = []

            days = get_months(int(start_time/1000),int(end_time/1000))

            for day in days:
                dates.append(day)
                index = -1
                for i, row in enumerate(result):
                    if str(row[0]) == day:
                        index = i

                if index == -1:
                    counts.append(0)
                    totals.append(0)
                    taxs.append(0)
                else:
                    temp = result[index]

                    counts.append(temp[1])
                    totals.append(int(temp[2]))
                    taxs.append(int(temp[3]))

            data = {}
            data['dates'] = dates
            data['counts'] = counts
            data['totals'] = totals
            data['taxs'] = taxs


            amount_list = amount_result[0]

            if amount_list[0]:
                data['count_total'] = int(amount_list[0])
            else:
                data['count_total'] = 0

            if amount_list[1]:
                data['total_total'] = int(amount_list[1])
            else:
                data['total_total'] = 0


            if amount_list[2]:
                data['tax_total'] = int(amount_list[2])
            else:
                data['tax_total'] = 0


            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data

        finally:
            session.close()
            json_rsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(json_rsp)


class StatisticsMonthHandler(tornado.web.RequestHandler):
    def get(self):
        logger.info('===here')
        start_time = int(self.get_argument('start_time'))
        end_time = int(self.get_argument('end_time'))
        request_type = 0
        store_id = 1
        district = ''
        devices = self.get_argument('devices','no')
        if devices != 'no':
            request_type = 1
        else:
            store_id = self.get_argument('store_id', 0)
            if store_id != 0:
                request_type = 2
            else:
                district = self.get_argument('district', '')
                request_type = 3

        session = Session()
        resdic = {}
        try:
            if request_type == 1:
                devices_list = eval(devices)
                result = session.query(func.date_format(Deal.datetime, '%Y-%m-%d'), \
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)).\
                                 filter(Deal.time.between(start_time, end_time), \
                                            Deal.device_sn.in_(devices_list)).\
                                 group_by(func.date_format(Deal.datetime, '%Y-%m-%d')).all()

                amount_result = session.query(
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)).\
                                 filter(Deal.time.between(start_time, end_time), \
                                              Deal.device_sn.in_(devices_list)).all()
            elif request_type == 2:
                result = session.query(func.date_format(Deal.datetime, '%Y-%m-%d'), \
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), \
                           Deal.store_id==store_id). \
                    group_by(func.date_format(Deal.datetime, '%Y-%m-%d')).all()

                amount_result = session.query(
                    func.count('*'),
                    func.sum(Deal.total_price),
                    func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), Deal.store_id == store_id).all()
            elif request_type == 3:
                logger.info('=================')
                logger.info(district)
                result = session.query(func.date_format(Deal.datetime, '%Y-%m-%d'), \
                                       func.count('*'),
                                       func.sum(Deal.total_price),
                                       func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), Deal.store_id == Store.store_id, Store.district == district). \
                    group_by(func.date_format(Deal.datetime, '%Y-%m-%d')).all()
                amount_result = session.query(
                    func.count('*'),
                    func.sum(Deal.total_price),
                    func.sum(Deal.tax)). \
                    filter(Deal.time.between(start_time, end_time), Deal.store_id == Store.store_id, Store.district == district).all()

        except Exception, e:
            session.rollback()

            logger.error(e.message)

            resdic['code'] = 101
            resdic['message'] = 'statics failed'
            resdic['data'] = None
        else:
            dates = []
            counts = []
            totals = []
            taxs = []

            days = get_days(int(start_time / 1000), int(end_time / 1000))

            for day in days:
                dates.append(day)
                index = -1
                for i, row in enumerate(result):
                    if str(row[0]) == day:
                        index = i

                if index == -1:
                    counts.append(0)
                    totals.append(0)
                    taxs.append(0)
                else:
                    temp = result[index]

                    counts.append(temp[1])
                    totals.append(int(temp[2]))
                    taxs.append(int(temp[3]))

            data = {}
            data['dates'] = dates
            data['counts'] = counts
            data['totals'] = totals
            data['taxs'] = taxs

            amount_list = amount_result[0]

            if amount_list[0]:
                data['count_total'] = int(amount_list[0])
            else:
                data['count_total'] = 0

            if amount_list[1]:
                data['total_total'] = int(amount_list[1])
            else:
                data['total_total'] = 0


            if amount_list[2]:
                data['tax_total'] = int(amount_list[2])
            else:
                data['tax_total'] = 0

            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data

        finally:
            session.close()
            json_rsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(json_rsp)


class StoreHandler(tornado.web.RequestHandler):
    def get(self):
        store_id =  self.get_argument('store_id')

        # print 'gid'
        # import os
        # print(os.getpid())
        #
        #
        # from threading import current_thread
        #
        # thread = current_thread()
        # print thread.getName()

        session = Session()

        try:
            store = session.query(Store).filter_by(sn=store_id).first()
        except Exception,e:
            session.rollback()
            logger.info(e)
            resdic = {}
            resdic['code'] = 101
            resdic['message'] = 'devices failed'
            resdic['data'] = None
        else:
            list = []
            for obj in store.devices:
                device_sn = obj.sn
                list.append(device_sn)

            data = {}
            data['devices_list'] = list
            data['name'] = store.name
            data['location'] = 'Jakarta (Main Branch) Wisma GKBI suite 2201 Jalan Jendral Sudirman No.28 Jakarta 10210 Indonesia'

            resdic = {}

            resdic['code'] = 0
            resdic['message'] = 'success'
            resdic['data'] = data

        finally:
            session.close()
            json_rsp = json.dumps(resdic)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            headers = self.request.headers
            orgin = headers.get('Origin')
            if orgin:
                self.add_header("Access-Control-Allow-Origin", orgin)
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(json_rsp)