#coding=utf-8


from redis_manager import r_devcie_heart,r_online_device
import time
from super_models.history_model import OfflineHistroy,EventsHistroy
from super_models.database import Session
from super_models.store_model import Store
from super_models.device_model import Device


def get_last_online_time(device_sn):
    last = r_devcie_heart.get(device_sn)
    if last:
        return int(last)
    else:
        return 0

def offline_history(device_sn,new_time):
    last_time = get_last_online_time(device_sn)
    peroid = new_time - last_time
    if last_time != 0 and peroid > 120:
        session = Session()
        try:
            store = session.query(Store).filter(Device.sn == device_sn, Store.store_id == Device.store_id).first()
        except Exception, e:
            print e
        else:
            history = EventsHistroy()
            history.type = 1
            history.status = 0
            history.store_id = store.store_id
            history.device_sn = device_sn
            history.store_name = store.name
            history.start_time = last_time
            history.end_time = new_time
            history.time = new_time
            history.time_between = peroid
            try:
                session.add(history)
                session.commit()
            except Exception,e:
                print e
            finally:
                session.close()
        finally:
            session.close()


def update_online_device(device_sn):
    device_str = str(device_sn)
    current_time = int(time.time())

    offline_history(device_str,current_time)

    # 在线统计
    r_online_device.set(device_str,current_time)
    r_online_device.expire(device_str,60)

    # 最后一次在线时间
    r_devcie_heart.set(device_str,current_time)


def get_online_devices():
    return r_online_device.keys()



def check_online(device_sn):
    last_time = r_online_device.get(device_sn)
    if last_time:
        return True
    else:
        return False


if __name__ == '__main__':
    device_sn = '6201001000002'
    session = Session()
    try:
        store = session.query(Store).filter(Device.sn== device_sn,Store.store_id ==Device.store_id).first()
    except Exception,e:
        print e
    else:
        print store.name