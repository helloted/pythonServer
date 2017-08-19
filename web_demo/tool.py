#coding=utf-8

import urllib,urllib2
import json
import datetime
import time,random
from log_util.device_logger import logger
from redis_manager import redis_center
# from device_server.controllers.push_device_controller import send_printer
import requests

headers = {'Origin': '127.0.0.1'}

# url = 'http://127.0.0.1:5041/'

url = 'http://47.74.130.48:8041/'


def statistics():
    global url
    url = url + 'statistics/devices'
    current_milli_time = lambda: int(round(time.time() * 1000))
    textmod = {'devices': ['6201001000001',], 'start_time': current_milli_time()-1000 * 60 * 60 * 24 * 6 , 'end_time': current_milli_time()}
    print textmod
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()


def statistics_year():
    global url
    url = url + 'statistics/month'
    current_milli_time = lambda: int(round(time.time() * 1000))
    textmod = {'store_id':4, 'start_time': current_milli_time()-1000 * 60 * 60 * 24 * 365 , 'end_time': current_milli_time()}
    print textmod
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()


def statistics_month():
    global url
    url = url + 'statistics/day'
    current_milli_time = lambda: int(round(time.time() * 1000))
    textmod = {'store_id':1, 'start_time': current_milli_time()-1000 * 60 * 60 * 24 * 30 , 'end_time': current_milli_time()}
    print textmod
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def store():
    global url
    url = url + 'store'
    textmod = {'store_sn': 'INA000000001'}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def history_store():
    global url
    url = url + 'history/store'
    textmod = {'store_sn': 'INA000000001','index':1,'amount':10}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def history_device():
    global url
    url = url + 'history/devices'
    current_milli_time = lambda: int(round(time.time() * 1000))
    textmod = {'devices': ['6201001000002',],'index':1,'amount':10,'start_time':0,'end_time':current_milli_time()}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def history_detail():
    global url
    url = url + 'history/devices'
    textmod = {'devices': ['6201001000002',],'index':1,'amount':10}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()


def print_content():
    meal1 = ['Ginger & Pineapple Chicken',50000]
    meal2 = ['Kung Pao Chicken',78000]
    meal3 = ['prawn cocktail',54000]
    meal4 = ['satay chicken', 61000]
    meal5 = ['steamed pork dumplings', 26000]
    meal6 = ['roast peking duck', 55000]
    meal7 = ['sweet and sour king prawns', 90000]
    meal8 = ['kung po prawns', 67000]
    meal9 = ['prawn in chilli', 39000]
    meal10 = ['sweet and sour slicea fish', 94000]
    meal11= ['quick fried squid', 53000]
    meal12 = ['sur fried squid prawns and scallops in birds nest',88000]
    meal13 = ['chicken, Shrimp, Squid Mixed Vegetable ', 206000]
    meal14 = ['big Hamberger', 48000]
    meal15 = ['orenge Juice', 40000]
    meal16 = ['prawn cocktail', 66000]
    meal17 = ['crispy sqring rolls', 36000]
    meal18 = ['szechuan style lettuce wraps', 33000]
    meal19 = ['crispy seaweed', 109000]
    meal20 = ['sweet & Sour Chicken ', 8000]

    mealist = [meal1,meal2,meal3,meal4,meal5,meal6,meal7,meal8,meal9,meal10,meal11,meal12,meal13,meal14,meal15,meal16,meal17,meal18,meal19,meal20]

    result = random.sample(mealist, random.randint(2, 10))

    total = 0
    list = []
    for meal in result:
        qt =  random.randint(1, 3)
        price = meal[1]
        sub_total = qt * price
        total += sub_total
        name = meal[0]

        item = {'name': name, 'quantity': qt, 'subtotal': sub_total}

        list.append(item)

    dict = {}

    dict['total_price'] = 87000
    dict['items'] = 'tu dousi'

    global url
    url = url + 'print_content'
    data = {"device_sn": '6201001000002','post_time':100, "content": dict}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)

    print response.read()


def devices():
    global url
    url = url + 'devices'
    paras = {'page':1,'amount':10}
    resp = requests.get(url,paras)
    print resp.json()

def devices_fliter():
    global url
    url = url + 'devices/filter'
    paras = {'page':1,'amount':10}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url,json.dumps(paras))
    print resp.json()

def device_detail():
    global url
    url = url + 'device_detail'
    paras = {'device_sn':'6201001000000'}
    resp = requests.get(url,paras)
    print resp.json()

def device_setting():
    global url
    url = url + 'device_setting'
    paras = {'device_sn':'6201001000000','wifi_name':'HelloWifi','bluetooth_white_list':['456','4343'],'ip_white_list':'ip_white_list'}
    resp = requests.post(url,json.dumps(paras))
    print resp.json()

def update_app():
    global url
    url = url + 'app_update'
    paras = {'device_sn':'6201001000000','newest_url':'http://47.74.130.48:8005/files/app/capturer_2_2.0.apk'}
    resp = requests.post(url,json.dumps(paras),headers=headers)
    print resp.json()


def onlines():
    global url
    url = url + 'statistics/online'
    textmod = {'start_time': int(time.time())-60*60*24 , 'end_time': int(time.time())}
    print textmod
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

if __name__ == '__main__':
    a = 'hello:what::nihao'
    print a.replace(':', '')
