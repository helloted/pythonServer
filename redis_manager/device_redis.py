#coding=utf-8


from redis_manager import r_devcie_heart,r_online_device
import time


def update_online_device(device_sn):
    device_str = str(device_sn)
    current_time = int(time.time())

    # 在线统计
    r_online_device.set(device_str,current_time)
    r_online_device.expire(device_str,60)

    # 最后一次在线时间
    r_devcie_heart.set(device_str,current_time)


def get_online_devices():
    return r_online_device.keys()


def get_last_online_time(device_sn):
    last = r_devcie_heart.get(device_sn)
    if last:
        return int(last)
    else:
        return 0


def check_online(device_sn):
    last_time = r_online_device.get(device_sn)
    if last_time:
        return True
    else:
        return False