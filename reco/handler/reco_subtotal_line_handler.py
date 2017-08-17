# coding:utf-8

from reco.util import utils

"""
判断该行数据是否是subtotal行
若此算法判断通过则推荐使用get_subtotal方法解析
@:param keyword 用于判断改行是否为subtotal行
实用举例:
Subtotal                    30000
"""


def is_subtotal_line(items, keys):
    has_key = False
    if list(keys).__len__() > 0:
        has_key = True

    is_all_in = True
    for key in keys:
        if key not in items:
            is_all_in = False

    is_subtotal_format = False
    if items.__len__() == 2 or 3:
        items_first = str(items[0]).lower()
        items_last = utils.parse_format_price(items[items.__len__() - 1])
        if type(items_first) == str \
                and (type(items_last) == int or type(items_last) == float):
            is_subtotal_format = True

    return has_key and is_all_in and is_subtotal_format


def get_subtotal(items):
    return utils.parse_format_price(items[items.__len__() - 1])


if __name__ == "__main__":
    print "开始"
    lst = ["Subtotal","999,,.99"]
    print is_subtotal_line(lst, "subtotal")
    print get_subtotal(lst)
    print "结束"