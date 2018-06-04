#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
APP—Server的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from flask import Flask
from flask import request,redirect
from log_util.qr_logger import logger
from flask import render_template
from models.database import SessionContext
from models.QRmodel import QRModel
from models.applyModel import ApplyModel
from models.scan_history_model import ScanHistoryModel
from log_util import qr_logger
import time

app = Flask(__name__)

@app.route('/<value>', methods=['GET'])
def for_customer(value):
    return 'Please Use Clubori App to Scan this QR Code'


@app.route('/<qr_code>/', methods=['GET'])
def merchant_vercode(qr_code):
    token = request.args.get('token')
    uid = request.args.get('uid')
    if not uid or not token:
        return 'Please Login First'

    uid = int(uid)

    logger.info('qrcode is {qr}'.format(qr=qr_code))

    loc = request.args.get('loc')
    lat = None
    lng = None
    if loc:
        arr = loc.split(',')
        lat = arr[0]
        lng = arr[1]

        if lat:
            lat = float(lat)
            lng = float(lng)

    if not qr_code:
        return 'Invailed Qrcode'
    if qr_code == '1abcdefghijk':
        return render_template('/success.html',company='Apple Inc',product='Iphone X')

    else:
        with SessionContext() as session:
            scan_history = ScanHistoryModel()

            scan_history.merchant_id = uid
            scan_history.code = str(qr_code)
            scan_history.time = int(time.time())
            if lat:
                scan_history.lat = lat

            if lng:
                scan_history.lng = lng

            session.add(scan_history)
            session.commit()

            qr = session.query(QRModel).filter(QRModel.code==str(qr_code)).first()
            if qr:
                success_url = '/results/success.html?company={company}&product={product}'.format(company='Not Dispatch', product='Not Dispatch')
                return redirect(success_url)
            else:
                return redirect('/results/failed.html')


if __name__ == '__main__':
    app.run(port=5002)