#coding=utf-8

# import sys, os;sys.path.append(os.path.realpath("../.."))
import os
import socket
import time
import struct
import json
from tool import current_time_msec,current_time
import hashlib
from tool import aes_enc_b64

# host = "localhost"
# port = 5050
import random

host = '47.74.130.48'
port = 8050

ADDR = (host, port)

client = socket.socket()
client.connect(ADDR)

device_sn = "6201001000000"

def init_connect():

    sign = '122|'+device_sn

    signenc = aes_enc_b64(sign)

    initdata = {"cmd": "init_connect",
                "content": {"serail_num": device_sn,
                            "sign": signenc
                            },
                "seq": 1,
                "version": "1"
                }

    body = json.dumps(initdata)
    header = body.__len__()
    headPack = struct.pack("!1I", header)
    sendData = headPack + body.encode()

    client.send(sendData)
    res = client.recv(1024)
    print 'response:', res


def adddeal():
    a = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
    b = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))

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

    # print result
    #
    #
    # item1 = {'name': 'Big Hamberger', 'quantity': 1, 'subtotal': 8000}
    # item2 = {'name': 'Orenge Juice', 'quantity': 2, 'subtotal': 9000}
    #
    # list = (item1, item2)

    seed_token = 'seed'

    time = current_time_msec()

    text = device_sn + seed_token + str(time)
    base = aes_enc_b64(text)
    hah = hashlib.sha1(base).hexdigest()

    verify = hah[:6]

    deal_sn = device_sn + str(time)[:-3] + verify


    data1 = {"cmd": "upload_deal",
             "content": {"list": list,
                         'device_sn': device_sn,
                         'deal_sn': deal_sn,
                         'total_price': total,
                         'deal_time': time
                         },
             "seq": 5,
             "version": "1",
             }

    print data1

    body = json.dumps(data1)
    header = body.__len__()
    headPack = struct.pack("!1I", header)
    sendData1 = headPack + body.encode()
    client.send(sendData1)
    res = client.recv(1024)
    print 'response:', res


def heart_beat():
    data2 = {"cmd": "heart_beat",
             "seq": 3,
             "version": "1",
             'content':{'changed':False}
             }

    body = json.dumps(data2)
    header = body.__len__()
    headPack = struct.pack("!1I", header)

    sendData1 = headPack + body.encode()

    client.send(sendData1)

    res = client.recv(1024)
    print 'response:', res



if __name__ == '__main__':
    init_connect()
    while True:
        time.sleep(5)
        heart_beat()


