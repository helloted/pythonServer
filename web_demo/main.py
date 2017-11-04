#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.12
web_demo Server入口
"""

import sys, os; sys.path.append(os.path.realpath("../"))
from tornado import web, httpserver, ioloop
from tornado.options import options, define
from handlers import HistoryDevicesHandler,HistoryStoreHandler,StoreHandler,DealDetailHandler,StatisticsDeviceHandler,HistoryDistrictHandler
from handlers import StatisticsYearHandler,StatisticsMonthHandler
from live_handler import LiveHandler, PrintHandler
import threading
import time
import server_communicate
from web_demo.device_handler import DevicesHandler,DeviceDetailHandler,DeviceSettingHandler,DevicesFilterHandler,APPUpdateHandler,APPListHandler
from web_demo.device_handler import StatisticsOnlineHandler,LoginHandler, LogoutHandler
from web_demo.new_handler import AllStores,OfflineHistoryHandelr

define(name='port', default=5041, type=int)

def run_webserver():
    options.parse_command_line()
    app = web.Application(handlers=[(r"/live", LiveHandler),
                                    (r"/store", StoreHandler),
                                    (r"/history/devices", HistoryDevicesHandler),
                                    (r"/history/store", HistoryStoreHandler),
                                    (r"/history/district", HistoryDistrictHandler),
                                    (r"/deal_detail", DealDetailHandler),
                                    (r"/print_content", PrintHandler),
                                    (r"/devices", DevicesHandler),
                                    (r"/devices/filter", DevicesFilterHandler),
                                    (r"/device_detail", DeviceDetailHandler),
                                    (r"/device_setting", DeviceSettingHandler),
                                    (r"/app_list", APPListHandler),
                                    (r"/statistics/online", StatisticsOnlineHandler),
                                    (r"/user/login", LoginHandler),
                                    (r"/user/logout", LogoutHandler),
                                    (r"/statistics/month", StatisticsYearHandler),
                                    (r"/statistics/day", StatisticsMonthHandler),
                                    (r"/stores", AllStores),
                                    (r"/offline_historys", OfflineHistoryHandelr),
                                    (r"/statistics/devices", StatisticsDeviceHandler)])
    app.settings = {'cookie_secret':'e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d'}
    http_server = httpserver.HTTPServer(app,xheaders=True)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    # socket_server_thread = threading.Thread(target=server_communicate.socket_run, name='socket_server_thread')
    # socket_server_thread.start()

    run_webserver()