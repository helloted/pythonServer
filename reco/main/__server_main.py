# coding:utf-8

import json
import re

from flask import Flask, request

import reco_to_txt
import txt_to_result
from reco.main import reco_main


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/reco', methods=['GET', 'POST'])
def parse():
    data = request.form['data']
    print "源数据"
    print "data="+data

    temp = json.loads(data)
    print temp

    _reco_main = reco_main.RecoMain(temp)
    result = _reco_main.parse()

    fan = list()
    for r in result:
        fan_temp = dict()
        fan_temp.setdefault("cmd", r[0])
        fan_temp.setdefault("logo", r[1])
        fan.append(fan_temp)
    t = json.dumps(fan)

    print t
    return t



if __name__ == '__main__':
    app.run(host='192.168.0.66', port=5000, debug=True)