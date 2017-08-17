
import os
import hashlib
import time
import datetime

super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
ali_path = 'http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/'

i = 0

def image_save(user_id,image):
    global i
    i +=1
    if i == 10000:
        i = 1
    img_type = image.content_type.split('/', 1)[1]
    orgin = str(user_id) + str(int(time.time())) + str(datetime.datetime.now().microsecond) + str(i)
    img_name = hashlib.md5(orgin).hexdigest()
    full_name = img_name + '.' + img_type
    folder_path = super_path + '/ali_oss/temp'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image.save(folder_path + '/' + full_name)
    download_path = ali_path + full_name
    return download_path


