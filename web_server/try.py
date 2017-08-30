import urllib,urllib2
import json
import datetime
import time,random
from log_util.device_logger import logger
from redis_manager import redis_center
# from device_server.controllers.push_device_controller import send_printer
import requests

headers = {'Origin': '127.0.0.1'}

url = 'http://47.74.130.48:8042/'

# url = 'http://127.0.0.1:5042/'

def edit_status():
    global url
    url = url + 'events/edit_status'
    paras = {'id':51,'status':0}
    resp = requests.post(url,json.dumps(paras),headers=headers)
    print resp.text


if __name__ == '__main__':
    edit_status()