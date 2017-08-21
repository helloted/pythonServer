#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.12
实时订单接口
"""
import time
import tornado.web
import tornado.gen
import tornadoredis
from tornado.escape import json_encode
from log_util.web_demo_logger import logger
from redis_manager import redis_center
from super_models.database import Session
from super_models.deal_model import Deal


class LiveHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client = tornadoredis.Client()
        self.client.connect()  # 连接到Redis

    @tornado.web.asynchronous
    def get(self):
        self.get_data()

    @tornado.web.asynchronous
    def post(self):
        self.get_data()

    @tornado.gen.engine
    def subscribe(self,channel):  # 订阅Redis的消息
        yield tornado.gen.Task(self.client.subscribe, channel)
        self.client.listen(self.on_message)

    def get_data(self):
        if self.request.connection.stream.closed():
            return

        # body = self.get_body_argument()

        store_id = self.get_argument('store_id')
        time_point_str = self.get_argument('time_point')

        time_point= int(time_point_str)



        current_milli_time = lambda: int(round(time.time() * 1000))
        now_point = current_milli_time()


        session = Session()

        wait = True

        # if time_point == 0:
        #     wait = True
        # else:
        #     try:
        #         deals = session.query(Deal).filter(Deal.store_sn==store_sn,Deal.time.between(time_point, now_point)).\
        #             order_by((Deal.time.desc())).all()
        #     except Exception,e:
        #         session.rollback()
        #         dict = {}
        #         dict['code'] = 103
        #         dict['msg'] = 'live failed'
        #
        #         self.send_data(json_encode(dict))
        #     else:
        #
        #         if deals:
        #             wait = False
        #
        #             logger.info('got,timepoint:' + time_point_str + ':::' + str(now_point))
        #             logger.info(deals)
        #
        #             list = []
        #             for obj in deals:
        #                 deal = {}
        #                 deal['device_sn'] = obj.device_sn
        #                 deal['deal_sn'] = obj.sn
        #                 deal['time'] = obj.time
        #                 deal['total_price'] = obj.total_price
        #                 list.append(deal)
        #
        #             data = {}
        #             data['time_point'] = now_point
        #             data['deals'] = list
        #
        #             dict = {}
        #             dict['code'] = 0
        #             dict['msg'] = 'success'
        #             dict['data'] = data
        #
        #             self.send_data(json_encode(dict))
        #         else:
        #             wait = True
        #             logger.info('live,timepoint:' + time_point_str + ':::' + str(now_point))
        #             logger.info(deals)
        #     finally:
        #         session.close()

        if wait:
            channel = 'live_deal' + str(store_id)
            self.subscribe(channel)
            num = 60  # 设置超时时间为60s
            tornado.ioloop.IOLoop.instance().add_timeout(
                time.time() + num,
                lambda: self.on_timeout(num)
            )

    def on_timeout(self, num):
        self.send_data(json_encode({'name': '', 'msg': ''}))
        if (self.client.connection.connected()):
            self.client.disconnect()

    def send_data(self, data):  # 发送响应
        if self._finished:
            return
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')
        logger.info(data)
        self.write(data)
        self.finish()

    # @tornado.web.asynchronous
    def on_message(self, msg):  # 收到了Redis的消息
        if self._finished:
            return
        if (msg.kind == 'message'):
            body = str(msg.body)
            bodydic = eval(body)

            dict = {}
            dict['code'] = 0
            dict['msg'] = 'success'

            current_milli_time = lambda: int(round(time.time() * 1000))
            now_point = current_milli_time()

            data_dic = {}
            data_dic['time_point'] = now_point
            data_dic['deals'] = (bodydic,)

            dict['data'] = data_dic
            self.send_data(json_encode(dict))
        elif (msg.kind == 'unsubscribe'):
            self.client.disconnect()

    def on_finish(self):
        if (self.client.subscribed):
            self.client.unsubscribe('channel_great');



class PrintHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client = tornadoredis.Client()
        self.client.connect()  # 连接到Redis

    @tornado.web.asynchronous
    def get(self):
        self.get_data()

    @tornado.web.asynchronous
    def post(self):
        self.get_data()

    @tornado.gen.engine
    def subscribe(self,channel):  # 订阅Redis的消息
        yield tornado.gen.Task(self.client.subscribe, channel)
        self.client.listen(self.on_message)

    def get_data(self):
        if self.request.connection.stream.closed():
            return

        body = self.request.body
        logger.info(body)

        body_dic = eval(body)
        device_sn = body_dic.get('device_sn')
        post_time = body_dic.get('post_time')

        channel = device_sn + str(post_time)

        self.subscribe(channel)

        redis_center.publish('cmd_print', body)

        num = 60  # 设置超时时间为60s
        tornado.ioloop.IOLoop.instance().add_timeout(
            time.time() + num,
            lambda: self.on_timeout(num)
        )

    def send_data(self, data):  # 发送响应
        if self._finished:
            return
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        headers = self.request.headers
        orgin = headers.get('Origin')
        if orgin:
            self.add_header("Access-Control-Allow-Origin", orgin)
        self.add_header("Access-Control-Allow-Credentials", 'true')
        logger.info(data)
        self.write(data)
        self.finish()

    def on_message(self, msg):  # 收到了Redis的消息
        if self._finished:
            return
        if (msg.kind == 'message'):
            body = str(msg.body)
            body_dic = eval(body)
            self.send_data(json_encode(body_dic))
        elif (msg.kind == 'unsubscribe'):
            self.client.disconnect()

    def on_finish(self):
        if (self.client.subscribed):
            self.client.unsubscribe('channel_great');

    def on_timeout(self, num):
        self.send_data(json_encode({'name': '', 'msg': ''}))
        if (self.client.connection.connected()):
            self.client.disconnect()