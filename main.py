#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
APP—Server的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Flask,session
from layers.merchantLayer import node_merchant
from layers.managerLayer import node_manager
from layers.agentLayer import node_agent
from layers.dipatchLayer import node_dispatch
from datetime import timedelta


app = Flask(__name__)

app.secret_key = 'A0Zr98jkhekd'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=60*60*24)

app.register_blueprint(node_merchant, url_prefix='/merchant')
app.register_blueprint(node_manager, url_prefix='/manager')
app.register_blueprint(node_agent, url_prefix='/agent')
app.register_blueprint(node_dispatch, url_prefix='/dispatch')


if __name__ == '__main__':
    app.run(port=5001)