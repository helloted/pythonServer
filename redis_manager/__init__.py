#coding=utf-8

import redis

redis_center = redis.Redis(host='127.0.0.1', port=6379, db=1)

redis_web_center = redis.Redis(host='127.0.0.1', port=6379, db=11)