
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from redis_manager import r_queue
import time




def update_token():
    data = {}
    data['device_sn'] = '6201001000003'
    data['type'] = 'update_token'
    r_queue.lpush('devices_queue', data)



def kill_sokcet(device_sn):
    data = {}
    data['device_sn'] = device_sn
    data['type'] = 'kill_socket'
    r_queue.lpush('devices_queue', data)


if __name__ == '__main__':
    kill_sokcet('6201001000002')
