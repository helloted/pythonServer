
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import requests
import json

url = 'http://127.0.0.1:5001/'

# url = 'http://clubori.com/api/'

headerdata = {"Content-type": "application/json"}

def ver_code():
    global url
    url = url + 'merchant/ver_code'
    para = {'email':'helloworld@qq.com'}
    res = requests.get(url,params=para)
    print res.content


def register():
    global url
    url = url + 'merchant/register'
    para = {'email':'helloworld@qq.com','name':'hello','phone':'3984343','password':'wooddiekd','brand':'iphone','ver_code':7389}
    res = requests.post(url,data=json.dumps(para),headers=headerdata)
    print res.content


def login():
    global url
    url = url + 'merchant/login'
    para = {'phone':'3984343','password':'wooddiekd'}
    res = requests.post(url,data=json.dumps(para),headers=headerdata)
    print res.content


def agent_register():
    global url
    url = url + 'agent/register'
    para = {'email':'agent_1@qq.com','name':'agent_1','phone':'10001','password':'111111'}
    res = requests.post(url,data=json.dumps(para),headers=headerdata)
    print res.content


def agent_login():
    global url
    url = url + 'agent/login'
    para = {'phone':'10001','password':'111111'}
    res = requests.post(url,data=json.dumps(para),headers=headerdata)
    print res.cookies
    print res.content


def generate():
    global url
    url = url + 'manager/generate?phone=100001'
    para = {'count':1000,}
    res = requests.post(url,data=json.dumps(para),headers=headerdata)
    print res.content


def generate_list():
    global url
    url = url + 'manager/generate_list'
    para = {'count':100,}
    res = requests.get(url)
    print res.content


def delete_code():
    global url
    url = url + 'manager/delete'
    para = {'history_sn':1523588324,}
    res = requests.get(url,params=para)
    print res.content


def agent_apply():
    global url
    url = url + 'agent/apply?agent_id=2'
    para = {'company':'Apple','brand':'Iphone X','count':1000,'others':{'model':'64G'}}
    res = requests.post(url, data=json.dumps(para), headers=headerdata)
    print res.content


def apply_list():
    global url
    url = url + 'agent/apply_list?agent_id=1'
    res = requests.get(url)
    print res.content


def manager_apply_list():
    global url
    para = {'agent_id': 1,'token':'+zT5MuOiTS3Y/14X/VxuCbHCzemqTxXoufPsV/K5N0g='}
    cook = {'agent_id':1}
    url = url + 'manager/apply_list'
    res = requests.get(url,params=para)
    print res.content


def dispatch():
    global url
    para = {'agent_id': 1,'token':'+zT5MuOiTS3Y/14X/VxuCbHCzemqTxXoufPsV/K5N0g=','apply_sn':'2_1523604032'}
    url = url + 'manager/dispatch'
    res = requests.get(url,params=para)
    print res.content


def session_try():
    global url
    s = requests.Session()
    url = url + 'manager/hello'
    res = s.get(url)
    print res.content
    print '22========'
    res = s.get(url)
    print res.content

if __name__ == '__main__':
    apply_list()