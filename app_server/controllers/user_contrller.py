#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
User处理
"""

from app_server.models.user_model import User
from super_models.database import SessionContext
from app_server.response import dberror_handle
import time
import hashlib
from super_controllers.id_dispath import get_user_id

def user_add(phone,password):
    with SessionContext(dberror_handle) as session:
        user = User()
        user_id = get_user_id()
        if user_id:
            user.phone = phone
            user.password = password
            user.user_id = user_id
            user.name = 'Fresh'
            user.icon = 'http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/default_app_icon.png'

            current_time = int(time.time())
            user.register_time = current_time

            session.add(user)
            session.commit()


def product_token(phone):
    current_milli_time = lambda: int(round(time.time() * 1000))
    current_time_str = str(current_milli_time())
    temp = phone + current_time_str + 'akey'
    token = hashlib.sha1(temp).hexdigest()
    return token


if __name__ == '__main__':
    # arr = [1,2,3,4,5,6,7,8,9,0]
    # result = random.sample(arr, random.randint(6, 6))
    print 'success'


