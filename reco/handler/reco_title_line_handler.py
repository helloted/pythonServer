# coding:utf-8

"""
判断该行是否为订单title行
判断通过条件:所有key必须同时存在于改行
"""


def is_title(items, keys):
    has_key = False
    if list(keys).__len__() > 0:
        has_key = True

    is_all_in = True
    for key in keys:
        if key not in items:
            is_all_in = False
            break
    return has_key and is_all_in


"""
解析出订单id
"""


def get_title(items):
    return " ".join(items)

