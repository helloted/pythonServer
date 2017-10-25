#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.27
WEB—Server的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Flask
from web_server.layers.event_layer import node_event
from web_server.layers.device_layer import node_device
from web_server.layers.service import node_service
from web_server.layers.deal_convert_layer import node_deal_convert
from log_util.web_demo_logger import logger

app = Flask(__name__)


app.register_blueprint(node_event, url_prefix='/events')
app.register_blueprint(node_device, url_prefix='/device')
app.register_blueprint(node_service, url_prefix='/service')
app.register_blueprint(node_deal_convert, url_prefix='/deal_convert')



if __name__ == '__main__':
    logger.info('server run at 5042')
    app.run(port=5042)