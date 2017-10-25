import random
import string
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from super_models.device_key_model import DeviceKey
from super_models.database import Session
from super_models.device_model import Device
import time


def generator_key():
    orgin = '6201001000100'
    session = Session()
    for i in range(50):
        first_key = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        i_str = str(i)
        cut_str = orgin[:-len(i_str)]
        device_sn = cut_str + i_str
        print device_sn,first_key

        device_key = DeviceKey()
        device_key.device_sn = device_sn
        device_key.key = first_key
        device_key.version = 1
        device_key.time = int(time.time())
        session.add(device_key)

    session.commit()


def device_gen():
    orgin = '6201001000100'
    session = Session()
    for i in range(50):
        i_str = str(i)
        cut_str = orgin[:-len(i_str)]
        device_sn = cut_str + i_str
        print device_sn

        device = Device()
        device.sn = device_sn
        session.add(device)

    session.commit()

if __name__ == '__main__':
    device_gen()
