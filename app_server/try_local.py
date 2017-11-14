
import urllib,urllib2
import json
import datetime
import time,random
from log_util.device_logger import logger
from redis_manager import redis_center
# from device_server.controllers.push_device_controller import send_printer

url = 'http://127.0.0.1:5008/'

token = 'c4270974728b49b4b518231de9c48d5cf4ca0860'

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
    user_mod = {'user_id': 1,'token':token,'store_id':1,'store_id':2}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    print url
    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req)
    print res.read()

def store_update():
    global url
    url = url + 'store/update'
    data = {'store_id':1, 'lng':113.9425396505,'banners_list':['http://img.sj33.cn/uploads/allimg/201402/7-140206204500561.png',]}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()

def code():
    global url
    url = url + 'user/code'
    textmod = {'phone': 1430434343}
    textmod = urllib.urlencode(textmod)
    print(textmod)
    req = urllib2.Request(url='%s%s%s' % (url, '?', textmod))
    res = urllib2.urlopen(req)
    print res.read()


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
    url = url + 'user/update?user_id=1'
    data = {'name': 'jack'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def register():
    global url
    url = url + 'user/register'
    data = {'phone': 1430434343,'code':'506372','password':'apassword'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def password():
    global url
    url = url + 'user/password'
    data = {'phone': 1430434343,'code':'506372','password':'apassword'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()

def login():
    global url
    url = url + 'user/login'
    data = {'phone': '1430434343','password':'apassword'}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()

def logout():
    global url
    url = url + 'user/logout'
    user_mod = {'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def favorite():
    global url
    url = url + 'store/favorite'
    user_mod = {'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'store_id': 1,'add':True}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def article_add():
    global url
    url = url + 'article/add'
    user_mod = {'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'store_id': 1,'anonymous':True,'deal_sn':'this is dealsn','score':5,'per':5000,'text':'this store is very good one'}
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
    user_mod = {'article_id':5,'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def article_like():
    global url
    url = url + 'article/like'
    user_mod = {'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'article_id': 5,'add':True}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def article_favorite():
    global url
    url = url + 'article/favorite'
    user_mod = {'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'article_id': 5,'add':True}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def comment_add():
    global url
    url = url + 'article/comment_add'
    user_mod = {'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'article_id': 5,'type':1,'text':'this store is very good one','replied_user_id':1}
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


def mine_favorite_store():
    global url
    url = url + 'mine/favorite_store'
    user_mod = {'user_id': 1, 'token': token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def mine_post():
    global url
    url = url + 'mine/post'
    user_mod = {'user_id': 1, 'token': token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def mine_favorite_article():
    global url
    url = url + 'mine/favorite_article'
    user_mod = {'user_id': 1, 'token': token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    print response.read()


def like():
    global url
    url = url + 'article/like'
    user_mod = {'user_id': 1,'token':token}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    data = {'article_id': 5,'add':False}
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print response.read()


def store_filter():
    global url
    url = url + 'store/filter'
    user_mod = {'region_code':1,'page':1,'amount':10,'order':0,'open':0}
    url_mod = urllib.urlencode(user_mod)
    url = '%s%s%s' % (url, '?', url_mod)
    request = urllib2.Request(url=url)
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

if __name__ == '__main__':
    article_like()
