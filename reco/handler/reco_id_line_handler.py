# coding:utf-8

import re
from reco.main import const

"""
判断该行是否为订单id行
"""


def is_id(items, keys):
    has_key = False
    if list(keys).__len__() > 0:
        has_key = True

    is_all_in = True
    for key in keys:
        if key not in items:
            is_all_in = False
    return has_key and is_all_in


"""
解析出订单id
认为最后一个key后面第一个字符串就是id
例如:key1 key2 id
"""


def get_id(items, keys):
    start = items.index(keys[0])
    end = items.index(keys[len(keys)-1])
    line = "".join(items[start : end+2])
    reg_exp = "|".join(keys) + "|" + const.REG_EXP_SPECIAL_CHAR
    order_id = re.sub(reg_exp, "", line)
    return order_id

