#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.18
上线过机器统计
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from redis_manager import r_devcie_heart
import time
from datetime import datetime
from super_models.daily_model import Daily
from super_models.database import Session
from super_models.device_model import Device
from log_util.other_logger import logger

def tody_online():
    keys = r_devcie_heart.keys()
    online_account = 0
    for key in keys:
        value = r_devcie_heart.get(key)
        if not value:
            value = 0
        offline_time = int(value)
        if zero_point_time() < offline_time < zero_point_time() + 60*60*24:
            online_account += 1
    return online_account


def zero_point_time():
    cur_time = time.time()
    zero_time = cur_time - cur_time % 86400
    time_zone_zero = zero_time - 60 * 60 * 8
    return time_zone_zero


def save_date():
    session = Session()
    daily = Daily()
    onlin_amount = tody_online()
    record_time = int(time.time())
    try:
        device_amount = session.query(Device).count()

        daily.time = record_time
        daily.datetime = datetime.fromtimestamp(record_time)
        daily.total_device = device_amount
        daily.online_device = onlin_amount

        session.add(daily)
        session.commit()
    except Exception,e:
        logger.error(e)
    finally:
        session.close()


if __name__ == '__main__':
    save_date()
