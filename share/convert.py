import string
import random
import time

__radix_char = '8GSh3dg6OA1PtU2ycx5jDbukFXRzQa9Ip4rVWZm7Ms0lNqLiwCoYvTEBfKJHne'
__radix = len(__radix_char)
__ch2val = {}
__index = 0
for c in __radix_char:
    __ch2val[c] = __index
    __index += 1 

def itoa(num):
    result = ""
    while num > 0:
        result = __radix_char[num % __radix] + result
        num /= __radix
    return result 

def atoi(s):
    result = 0
    for c in s:
        result = __ch2val[c] + result * __radix
    return result

# def shuffle():
#     global __radix_char
#     ok_list = []
#     for i in range(0,62):
#         ok_list.append(i)
#     print ok_list
#     random.shuffle(ok_list)
#     result = ''
#     for i,val in enumerate(ok_list):
#         result += __radix_char[val]
#     __radix_char = result

def change(num):
    result = ""
    while num > 0:
        i = num % __count
        result = __my_char[i] + result
        print i,result
        num /= __radix
    return result

__my_char = string.digits + string.letters
__count = len(__my_char)


def restore(sn):
    print 'hello'

if __name__ == '__main__':
    # deal_sn = itoa(10615105432884776201001000002)
    # print deal_sn
    deal_sn = 'UsEGfusYXW545hD1928b0c'
    qr_sn = deal_sn[:-6]
    print atoi(qr_sn)
