import random
import json
import sys, os; sys.path.append(os.path.realpath("../"))
from super_models.deal_model import Deal
from share.tool import aes_enc_b64
import hashlib
import datetime
import time
from super_models.database import Session
import gevent
from redis_manager import redis_center

def insert_deal(device_sn,store_id,deal_time):

    stamp = int(deal_time/1000)
    hour = int(time.strftime('%H',  time.localtime(stamp)))
    if hour > 20 or hour < 9:
        return


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

    countlist = [1,2,3,3,4,4,4,5,5,5,5,6,6,6,6,6,7,7,7,8,8,9,10]

    num = random.randint(1, len(countlist)-1)

    count = countlist[num]

    result = random.sample(mealist, count)

    total = 0
    items_list = []
    for meal in result:
        qt =  random.randint(1, 3)
        price = meal[1]
        sub_total = qt * price
        total += sub_total
        name = meal[0]

        item = {'name': name, 'quantity': qt, 'subtotal': sub_total}

        items_list.append(item)

    seed_token = 'seed'

    text = device_sn + seed_token + str(deal_time)
    base = aes_enc_b64(text)
    hah = hashlib.sha1(base).hexdigest()

    verify = hah[:6]

    deal_sn = device_sn + str(deal_time)[:-3] + verify

    session = Session()

    try:
        deal = Deal()
        deal.sn = deal_sn
        deal.time = deal_time
        deal.datetime = datetime.datetime.fromtimestamp(deal_time / 1000)

        deal.device_sn = device_sn
        deal.store_id = store_id
        deal.total_price = int(total)
        deal.items_list = json.dumps(items_list)
        session.add(deal)
        session.commit()
    except Exception,e:
        print e
    else:
        live = {}
        live['store_id'] = store_id
        live['device_sn'] = device_sn
        live['deal_sn'] = deal_sn
        live['time'] = deal_time
        live['total_price'] = int(total)

        channel = 'live_deal' + str(store_id)

        redis_center.publish(channel, live)
    finally:
        session.close()

def device_auto_6():
    while True:
        gevent.sleep(random.randint(30,600))
        current_milli_time = lambda: int(round(time.time() * 1000))
        deal_time = current_milli_time()
        insert_deal('6201001000006',3,deal_time)


def device_auto_7():
    while True:
        gevent.sleep(random.randint(30,600))
        current_milli_time = lambda: int(round(time.time() * 1000))
        deal_time = current_milli_time()
        insert_deal('6201001000007',3,deal_time)


def device_auto_8():
    while True:
        gevent.sleep(random.randint(30,600))
        current_milli_time = lambda: int(round(time.time() * 1000))
        deal_time = current_milli_time()
        insert_deal('6201001000008',4,deal_time)


def auto_device():
    gevent.joinall([gevent.spawn(device_auto_6),
                    gevent.spawn(device_auto_7),
                    gevent.spawn(device_auto_8),
                    ])


if __name__ == "__main__":
    auto_device()

