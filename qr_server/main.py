#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
APP—Server的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Flask,render_template
from super_models.order_model import Order
from super_models.lottery_model import Lottery
from super_models.database import Session

app = Flask(__name__)


@app.route('/qr/<order_sn>')
def search_order(order_sn):
    session = Session()
    order = session.query(Order).filter(Order.order_sn==order_sn).first()
    if not order:
        return 'No such order'
    else:
        return render_template('order.html', origin=order.original_text)


if __name__ == '__main__':
    app.run(port=5009)