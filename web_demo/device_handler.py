#coding=utf-8

import tornado.web
from web_demo.db_tool import SessionContext
from web_demo.web_response import success_resp,failed_resp,failed_resp_full
from super_models.device_model import Device
from super_models.store_model import Store
from redis_manager import redis_center,redis_web_device
import redis_manager.device_redis as device_redis
import time
import json
from log_util.web_demo_logger import logger
import super_utils.comment as comment
import os,datetime
from sqlalchemy import func
from super_models.daily_model import Daily
from schedule.device_online import tody_online
from web_demo.utils.session import login_required


class DevicesFilterHandler(tornado.web.RequestHandler):
    @login_required
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')

        bodystr = self.request.body
        body = json.loads(bodystr)

        page = body.get('page')
        amount = body.get('amount')
        page_int = int(page)
        amount_int = int(amount)
        offset = (page_int-1) * amount_int

        device_sn = body.get('device_sn')

        problem = body.get('problem')
        store_name = body.get('store_name')
        has_online =body.has_key('online')

        with SessionContext() as session:
            data = {}

            query = session.query(Device)

            if store_name:
                query = query.filter(Store.name==store_name,Device.store_id==Store.store_id)

            if problem:
                query = query.filter_by(problem=problem)

            if device_sn:
                query = query.filter_by(sn=device_sn)

            if has_online:
                online = body.get('online')
                online_list = device_redis.get_online_devices()
                if online:
                    logger.info('check on line')
                    query = query.filter(Device.sn.in_(online_list))
                else:
                    logger.info('check not online')
                    query = query.filter(~Device.sn.in_(online_list))

            query = query.limit(amount_int).offset(offset)

            devices = query.all()
            total = len(devices)

            total_page = total / amount_int + 1
            data['page_total'] = total_page
            data['current_page'] = page_int
            data['amount'] = amount_int

            device_list = []
            for dev in devices:
                device = {}
                device['device_sn'] = dev.sn

                store = session.query(Store).filter_by(store_id=dev.store_id).first()
                device['store_id'] = store.store_id
                device['store_name'] = store.name

                device['online'] = device_redis.check_online(dev.sn)

                device['problem'] = False
                device_list.append(device)

            data['devices'] = device_list
            session.result = success_resp(data)

        self.write(session.result)


class DevicesHandler(tornado.web.RequestHandler):
    @login_required
    def get(self):
        page = self.get_argument('page')
        amount = self.get_argument('amount')

        page_int = int(page)
        amount_int = int(amount)
        offset = (page_int-1) * amount_int

        with SessionContext() as session:
            devices = session.query(Device).limit(amount_int).offset(offset).all()
            total = session.query(Device).count()

            data = {}
            total_page = total/amount_int + 1
            data['page_total'] = total_page
            data['current_page'] = page_int
            data['amount'] = amount_int


            device_list = []
            for dev in devices:
                device = {}
                device['device_sn'] = dev.sn

                store = session.query(Store).filter_by(store_id=dev.store_id).first()
                if store:
                    device['store_id'] = store.store_id
                    device['store_name'] = store.name
                else:
                    device['store_id'] = 0
                    device['store_name'] = 'no store'

                device['online'] = device_redis.check_online(dev.sn)

                device['problem'] = False
                device_list.append(device)

            data['devices'] = device_list

            print 'data',data
            session.result = success_resp(data)

        print session.result
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')
        self.write(session.result)


class DeviceDetailHandler(tornado.web.RequestHandler):
    @login_required
    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')

        device_sn = self.get_argument('device_sn')
        if not device_sn:
            self.write(failed_resp_full(1,'No devicesn'))
            return

        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=device_sn).first()
            data={}
            if device:
                data['device_sn'] = device.sn
                data['problem'] = device.problem
                data['phone'] = device.phone
                data['wifi_name'] = device.wifi_name
                data['wifi_password'] = device.wifi_password
                data['wifi_encrypt_type'] = device.wifi_encrypt_type
                data['capture_baudrate'] = device.capture_baudrate
                data['app_print_baudrate'] = device.app_print_baudrate
                data['app_received_baudrate'] = device.app_received_baudrate
                data['net_port'] = device.net_port
                data['app_version'] = device.app_version
                data['port_connecting'] = device.port_connecting
                data['add_qr'] = device.add_qr
                data['justification'] = device.justification

                wifi_list = device.wifi_list
                data['wifi_list'] = []
                if wifi_list:
                    data['wifi_list'] = json.loads(wifi_list)

                store = session.query(Store).filter_by(store_id=device.store_id).first()
                if store:
                    data['store_id'] = store.store_id
                    data['store_name'] = store.name
                else:
                    data['store_id'] = 0
                    data['store_name'] = 'no store'

                last_time = device_redis.get_last_online_time(device.sn)
                if not last_time:
                    last_time = 0
                data['last_online_time'] = last_time



                if device.bluetooth_white_list:
                    data['bluetooth_white_list'] = json.loads(device.bluetooth_white_list)
                else:
                    data['bluetooth_white_list'] = None

                if device.ip_white_list:
                    data['ip_white_list'] = json.loads(device.ip_white_list)
                else:
                    data['ip_white_list'] = None

                if device.cut_cmds:
                    data['cut_cmds'] = json.loads(device.cut_cmds)
                else:
                    data['cut_cmds'] = None

                if device.order_valid_keys:
                    data['order_valid_keys'] = json.loads(device.order_valid_keys)
                else:
                    data['order_valid_keys'] = None

                if device.order_invalid_keys:
                    data['order_invalid_keys'] = json.loads(device.order_invalid_keys)
                else:
                    data['order_invalid_keys'] = None

                session.result = success_resp(data)

        self.write(session.result)


class DeviceSettingHandler(tornado.web.RequestHandler):
    # @login_required
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')

        bodystr = self.request.body


        logger.info(bodystr)

        body = {}
        if bodystr:
            body = json.loads(bodystr)

        device_sn = body.get('device_sn')
        if not device_sn:
            self.write(failed_resp_full(1, 'No devicesn'))
            return

        print 'body',body



        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=device_sn).first()
            if device:
                for key in body:
                    # if key and not body[key]:
                    #     continue
                    if key == 'bluetooth_white_list' or key == 'ip_white_list' or key =='cut_cmds' or key =='order_invalid_keys' or key =='order_valid_keys':
                        device.__setattr__(key, json.dumps(body[key]))
                    else:
                        device.__setattr__(key, body[key])
                device.setting_time = int(time.time())
                session.commit()
                session.result = success_resp()

                content = {'device_sn':device.sn}
                redis_web_device.publish('cmd_setting', content)

            else:
                session.result = failed_resp_full(2,'no such device')

        self.write(session.result)


class APPUpdateHandler(tornado.web.RequestHandler):
    # @login_required
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')

        bodystr = self.request.body

        body = {}
        if bodystr:
            body = eval(bodystr)

        device_sn = body.get('device_sn')
        newest_url = body.get('newest_url')
        if not device_sn:
            self.write(failed_resp_full(1, 'No devicesn'))
            return

        print 'body',body
        with SessionContext() as session:
            device = session.query(Device).filter_by(sn=device_sn).first()
            if device:
                device.newest_url = newest_url
                session.commit()
                session.result = success_resp()

                redis_web_device.publish('cmd_update_app',body)
            else:
                session.result = failed_resp_full(2,'no such device')

        self.write(session.result)


class APPListHandler(tornado.web.RequestHandler):
    @login_required
    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')

        superpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
        folder = superpath + '/files/app'
        file_list = os.listdir(folder)
        data = []
        for file in file_list:
            file_dict = {}
            file_dict['name'] = file
            file_dict['time'] = int(os.path.getctime(folder+'/'+file))
            data.append(file_dict)
        resp = success_resp(data)
        self.write(resp)


def get_days(begin_time,end_time):
    date_list = []
    begin_date = datetime.datetime.fromtimestamp(begin_time)
    end_date = datetime.datetime.fromtimestamp(end_time)
    while begin_date <= end_date:
        date_str = begin_date.strftime('%Y-%m-%d')
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

class StatisticsOnlineHandler(tornado.web.RequestHandler):
    @login_required
    def get(self):
        start_time = int(self.get_argument('start_time'))
        end_time = int(self.get_argument('end_time'))

        data = {}
        date_list = []
        online_list = []
        offline_list = []
        total_list = []
        days = get_days(start_time,end_time)
        with SessionContext() as session:
            result = session.query(Daily).filter(Daily.time.between(start_time, end_time)).all()

            for day in days:
                sameindex= -1

                # 结果里找对应的
                for i,daily in enumerate(result):
                    date_time = daily.datetime.strftime('%Y-%m-%d')
                    if date_time == day:
                        sameindex = i

                date_list.append(day)
                if sameindex == -1:
                    today = datetime.datetime.now().strftime('%Y-%m-%d')
                    if day == today:
                        online = tody_online()
                        total = session.query(Device).count()
                        offline = total - online

                        online_list.append(online)
                        total_list.append(total)
                        offline_list.append(offline)
                    else:
                        online_list.append(0)
                        total_list.append(0)
                        offline_list.append(0)
                else:
                    daily = result[sameindex]

                    online = daily.online_device
                    total = daily.total_device
                    offline = total - online

                    online_list.append(online)
                    total_list.append(total)
                    offline_list.append(offline)

            data['dates'] = date_list
            data['online'] = online_list
            data['offline'] = offline_list
            data['total'] = total_list

            session.result = success_resp(data)

        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.add_header("Access-Control-Allow-Credentials", 'true')
        self.write(session.result)

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        bodystr = self.request.body
        body = json.loads(bodystr)

        name = body.get('name')
        password = body.get('password')

        print self.request.headers

        data = {}
        if name == 'admin' and password == 'admin':
            self.set_secure_cookie('session_save', name)
            data['code'] = 0
            data['msg'] = 'success'
        else:
            data['code'] = 3
            data['msg'] = 'name or password wrong'

        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.add_header("Access-Control-Allow-Credentials", 'true')
        self.write(json.dumps(data))
    #
    # def get(self):
    #     data = {}
    #     self.set_secure_cookie('session_save', 'hello')
    #     data['code'] = 0
    #     data['msg'] = 'success'
    #
    #     remote_ip = self.request.remote_ip
    #     print 'ip',remote_ip
    #     print self.request.headers
    #
    #     self.set_header('Content-Type', 'application/json; charset=UTF-8')
    #     self.add_header("Access-Control-Allow-Origin", "*")
    #     self.write(json.dumps(data))

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('session_save')
        data = {}
        data['code'] = 0
        data['msg'] = 'success'
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.add_header("Access-Control-Allow-Credentials", 'true')
        self.write(json.dumps(data))
