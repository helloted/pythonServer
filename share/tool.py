
import time
import base64
from Crypto.Cipher import AES


def current_time_msec():
    current_milli_time = lambda: int(round(time.time() * 1000))
    return current_milli_time()

def current_time():
    current = time.time()
    return int(current)

def aes_enc_b64(data,aes_key=None):
    if not aes_key:
       aes_key = '1234567890123456'
    size = AES.block_size
    count = size - len(data)%size
    if count is not 0:
        data+=(chr(0)*count)

    cipher = AES.new(aes_key)
    return base64.b64encode(cipher.encrypt(data))