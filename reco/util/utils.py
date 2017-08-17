# coding:utf-8

import json
import re
import time
import os


def is_json(ori):
    try:
        json.loads(str(ori))
    except ValueError:
        return False
    return True

"""
返回int 或者 float 或者 None
"""


def parse_format_price(num):
    try:
        temp = num
        if type(num) != str:
            temp = str(num)
        temp = re.compile(r",").sub("", temp)
        if is_int_price(temp):
            return int(temp)
        elif is_float_price(temp):
            return float(temp)
    except ValueError:
        return None
    return None


def is_int_price(ori):
    try:
        temp = re.compile(r",").sub("", ori)
        int(temp)
    except ValueError:
        return False
    return True


def is_float_price(ori):
    try:
        temp = re.compile(r",").sub("", ori)
        float(temp)
    except ValueError:
        return False
    return True


def can_to_number(ori):
    return is_int_price(ori) or is_float_price(ori)


def hex_to_str(s):
    base = '0123456789ABCDEF'
    i = 0
    s = s.strip().upper()
    s1 = ''
    while i < len(s):
        c1 = s[i]
        c2 = s[i + 1]
        i += 2
        b1 = base.find(c1)
        b2 = base.find(c2)
        if b1 == -1 or b2 == -1:
            return None
        s1 += chr((b1 << 4) + b2)
    return s1


def get_millisecond():
    return int(round(time.time() * 1000))


def get_root_path():
    return os.path.abspath(os.path.join(os.getcwd(), os.pardir))


def hex_add_blank(hex_str):
    result = ""
    if hex_str is not None:
        for i in range(len(hex_str)):
            result += hex_str[i]
            if i % 2 == 1:
                result += " "
    return result.strip(" ")


def hex_remove_blank(hex_str):
    if hex_str is not None and type(hex_str) == str:
        return str(hex_str).replace(" ", "")


if __name__ == "__main__":
    pass
    print hex_add_blank("")