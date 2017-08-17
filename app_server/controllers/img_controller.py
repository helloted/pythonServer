#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.05
上传图片
"""

import hashlib
import time
import os
import oss2

endpoint = 'http://oss-ap-southeast-1.aliyuncs.com' # Suppose that your bucket is in the Hangzhou region.
auth = oss2.Auth('LTAIluGfZlxp1UvU', 'YJmpbFVtbUJjDjZldYQEytyGa91aEs')
bucket = oss2.Bucket(auth, endpoint, 'swindtech-img')

def product_key(uid):
    current_milli_time = lambda: int(round(time.time() * 1000))
    current_time_str = str(current_milli_time())
    temp = uid + current_time_str + 'img_token'
    token = hashlib.md5(temp).hexdigest()
    return token


def formatSize(path):
    bytes = os.path.getsize(path)
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


def upload_img():
    super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,os.pardir))
    img_folder = super_path + '/server_img_temp'
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    for filename in os.listdir(img_folder):
        file_path = img_folder + '/' + filename
        file_object = open(file_path)
        result =  bucket.put_object(filename, file_object)
        if result.status == 200 and os.path.exists(file_path):
            os.remove(file_path)

    for object_info in oss2.ObjectIterator(bucket):
        print(object_info.key)



if __name__ == '__main__':
    upload_img()
    bucket.delete_object('story.txt')