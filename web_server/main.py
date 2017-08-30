#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.27
WEB—Server的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Flask
from web_server.layers.event_layer import node_event

app = Flask(__name__)


app.register_blueprint(node_event, url_prefix='/events')


if __name__ == '__main__':
    app.run(port=5042)