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
    paras = {'device_sn':'6201001000104','time':123456}
    resp = requests.post(url,json.dumps(paras),headers=headers)
    print resp.text


def update_app():
    global url
    url = url + 'device/app_update'
    paras = {'device_sn':'6201001000000','newest_url':'http://www.swindtech.com:8005/files/app/capturer_81_1.0.1.apk'}
    resp = requests.post(url,json.dumps(paras),headers=headers)
    print resp.text


def repeat_upload():
    global url
    url = url + 'device/repeat_upload_deal'
    paras = {'device_sn':'6201001000001','start_time':1509349352,'end_time':1509350352}
    resp = requests.post(url,json.dumps(paras),headers=headers)
    print resp.text

def interactive_setting_list():
    global url
    url = url + 'device/interactive_setting_list'
    resp = requests.get(url,headers=headers)
    print resp.text

def interactive_setting():
    global url
    url = url + 'device/interactive_setting'
    paras = {'device_sn':'6201001000000','type':1,'url':'www.baidu.com'}
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


def devices_list():
    global url
    url = url + 'device_info/list'
    paras = {'page': 1, 'amount': 10}
    resp = requests.get(url,paras)
    print resp.text


def device_detail():
    global url
    url = url + 'device_info/detail'
    paras = {'device_sn':'6201001000000'}
    resp = requests.get(url,paras)
    print resp.text


if __name__ == '__main__':
    interactive_setting()