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
"""


def get_id(items, keys):
    line = "".join(items)
    reg_exp = "|".join(keys) + "|" + const.REG_EXP_SPECIAL_CHAR
    order_id = re.sub(reg_exp, "", line)
    return order_id

