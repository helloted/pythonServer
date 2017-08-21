
from redis_manager import redis_center
import time

device_id = 1

live = {}
live['store_id'] = 1
live['device_id'] = device_id
live['deal_id'] = 1
live['deal_sn'] = 'slefesife83043'
live['time'] = 1497196800000
live['total_price'] = 10000


data = {"device_id": 1, "content": 'this is the content'}


if __name__ == '__main__':
    # redis_center.publish(str(device_id), live)
    while True:
        redis_center.publish('cmd_print', data)
        time.sleep(3)