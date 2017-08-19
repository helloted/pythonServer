
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from redis_manager import r_queue
import time

data = {}
data['device_sn'] = '6201001000003'
data['type'] = 'update_token'
r_queue.lpush('devices_queue', data)
