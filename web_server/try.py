import urllib,urllib2
import json
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

def upload_log():
    global url
    url = url + 'device/upload_log'
    paras = {'device_sn':'6201001000000','time':123456}
    resp = requests.post(url,json.dumps(paras),headers=headers)
    print resp.text


def service_id():
    global url
    url = url + 'service/dealID_scan'
    resp = requests.get(url)
    print resp.text

def deal_list():
    global url
    url = url + 'deal_convert/list'
    resp = requests.get(url)
    print resp.text

def deal_event():
    global url
    url = url + 'deal_convert/event'
    paras = {'deal_name':'62010010001001508835905ebffaf.txt','event':2}
    resp = requests.post(url,json.dumps(paras),headers=headers)
    print resp.text


if __name__ == '__main__':
    deal_list()