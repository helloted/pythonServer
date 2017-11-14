#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
APP—Server的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Flask
from super_models.order_model import Order
from super_models.lottery_model import Lottery
from super_models.database import Session

app = Flask(__name__)


@app.route('/qr/<order_sn>')
def search_order(order_sn):
  return 'this is the order of {order_sn}'.format(order_sn=order_sn)

if __name__ == '__main__':
    app.run(port=5009)