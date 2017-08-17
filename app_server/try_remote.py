
import urllib,urllib2
import json
import datetime
import time,random
from log_util.device_logger import logger
from redis_manager import redis_center
# from device_server.controllers.push_device_controller import send_printer

url = 'http://47.74.130.48:8008/'

user_id =2
token = '7bc6c144c258dfb5d4c2775d41980f4ebf1906c2'

def banner():
    global url
    url = url + 'homepage/banners'
    textmod = {'region_code': 1}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def hots():
    global url
    url = url + 'homepage/hots'
    textmod = {'region_code': 1}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()


def recommands():
    global url
    url = url + 'homepage/recommands'
    textmod = {'region_code': 1}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def homepage():
    global url
    url = url + 'homepage'
    textmod = {'region_code': 1}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def store():
    global url
    url = url + 'store'
    textmod = {'store_id': 1}
    textmod = urllib.urlencode(textmod)
    print('%s%s%s' % (url, '?', textmod))
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()


def store_update():
    global url
    url = url + 'store/update'
    data = {'store_id':1, 'favorites_amount':5,'menus_list':['http://img.sj33.cn/uploads/allimg/201402/7-140206204500561.png',]}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()

def code():
    global url
    url = url + 'user/code'
    textmod = {'phone': '138000001'}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def register():
    global url
    url = url + 'user/register'
    data = {'phone': '138000001','code':'481758','password':'apassword'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def login():
    global url
    url = url + 'user/login'
    data = {'phone':'138000000','password':'apassword'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def user():
    global url
    url = url + 'user'
    textmod = {'user_id':1,'token':'dad66ccf7eaa66aae1f6a368c42a9abb1b068228'}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()

def user_update():
    global url
    url = url + 'user/update'
    user_mod = {'user_id': user_id,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'name': 'new name','city':'hongkong'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()

def favorite():
    global url
    url = url + 'store/favorite'
    user_mod = {'user_id': 2,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'store_id': 1,'add':False}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()

def article_add():
    global url
    url = url + 'article/add'
    user_mod = {'user_id': user_id,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'store_id': 1,'anonymous':False,'deal_sn':'this is dealsn','score':5,'per':5000,'text':'this store is very good one'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def article_list():
    global url
    url = url + 'article/list'
    user_mod = {'store_id':1}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def article():
    global url
    url = url + 'article'
    user_mod = {'article_id':1,'user_id': user_id,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def comment_add():
    global url
    url = url + 'article/comment_add'
    user_mod = {'user_id': user_id,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'article_id': 1,'type':0,'text':'this is test comment'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def comments():
    global url
    url = url + 'article/comments'
    user_mod = {'article_id':1,'page':1,'amount':1}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


# def like():
#     global url
#     url = url + 'article/like'
#     user_mod = {'user_id': user_id,'token':token}
#     url_mod = urllib.urlencode(user_mod)
#     url = '%s%s%s' % (url, '?', url_mod)
#     data = {'article_id': 1,'add':False}
#     headers = {'Content-Type': 'application/json'}
#     request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
#     response = urllib2.urlopen(request)
#     print response.read()

def article_like():
    global url
    url = url + 'article/like'
    user_mod = {'user_id': user_id,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'article_id': 1,'add':True}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def goods_show():
    global url
    url = url + 'homepage/goods_show'
    user_mod = {'region_code':1,'page':1,'amount':10,'user_id':4}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def store_filter():
    global url
    url = url + 'store/filter'
    user_mod = {'region_code':1,'page':1,'amount':10,'lng':0,'lat':0,'order':0}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def store_list():
    global url
    url = url + 'store/filter'
    user_mod = {'region_code':1,'page':1,'amount':10,'lng':0,'lat':0,'order':0}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url) 
    response = urllib2.urlopen(request)
    print response.read()


def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()


if __name__ == '__main__':
    store_list()
