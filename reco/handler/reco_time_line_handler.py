# coding:utf-8

import time
import re


"""
判断该行是否为时间行
"""


def is_time(items, keys):
    has_key = False
    if list(keys).__len__() > 0:
        has_key = True

    is_all_in = True
    for key in keys:
        if key not in items:
            is_all_in = False
    return has_key and is_all_in


"""
解析出时间   返回字符串
"""


def get_time(items, keys):
    line = " ".join(items)
    reg_exp = "|".join(keys)
    time_str = re.sub(reg_exp, "", line)
    return time_str













def is_time_test(items):
    for item in items:
        word = str(item).lower().strip()
        if "am" == word or "pm" == word:
            return True
        if "time" in word:
            return True
    return False



"""
解析出时间 返回毫秒时间戳
"""
def get_time_test(items):
    if len(items) > 2:
        if "am" in " ".join(items) or "pm" in " ".join(items):
            return None
        else:
            timeStr = " ".join(items)
            timeStr = re.compile(r"[:/]").sub("-", timeStr)
            p = re.compile(r'\d{2,4}-\d{1,2}-\d{1,2} \d{2}-\d{1,2}-\d{1,2}')
            m = p.search(timeStr)
            if m:
                t = m.group(0)
                time_stamp = (int)(time.mktime(time.strptime(t, "%Y-%m-%d %H-%M-%S")))
                t = time_stamp * 1000
            else:
                t = None
            return t
    else:
        return None