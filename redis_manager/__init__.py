
import redis

redis_center = redis.Redis(host='localhost', port=6379, db=0)

r_online_device = redis.Redis(host='localhost', port=6379, db=1)

r_devcie_heart = redis.Redis(host='localhost', port=6379, db=2)

r_deal_sn= redis.Redis(host='localhost', port=6379, db=3)

r_queue= redis.StrictRedis(host='localhost', port=6379, db=4)

r_upload_token = redis.StrictRedis(host='localhost', port=6379, db=5)

