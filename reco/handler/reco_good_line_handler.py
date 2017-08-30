# coding:utf-8

import re

from reco.util import utils
from reco.main import const

"""
判断该行数据是否是商品详情行
items元素必须大等于3
若此算法判断通过则推荐使用get_good_301方法解析
实用举例:
Name            Qty             Subtotal     
Snow Affogato   *2              10000
Honey Chips     #3              10000.12
Gold Digger     ^4              10000
"""


def is_good_301(items):
    if len(items) >= 3:
        qty = re.sub(const.REG_EXP_SPECIAL_CHAR, "", items[len(items) - 2])
        if isinstance(items[0], str) \
                and utils.utils.is_int_price(qty) and int(qty) < 100 \
                and utils.can_to_number(items[len(items)-1]) and float(utils.parse_format_price(items[len(items)-1])) > 100:
            return True
        else:
            return False
    else:
        return False


def get_good_301(items):
    if len(items) >= 3:
        name = " ".join(items[0:(len(items)-2)])
        qty = re.sub(const.REG_EXP_SPECIAL_CHAR, "", items[len(items)-2])
        subtotal = utils.parse_format_price(items[len(items) - 1])
        unit_price = subtotal / qty
        good = dict()
        good.setdefault(const.GOOD_NAME, name)
        good.setdefault(const.GOOD_QTY, qty)
        good.setdefault(const.GOOD_UNIT_PRICE, unit_price)
        good.setdefault(const.GOOD_SUBTOTAL, subtotal)
        return good


"""
判断该行数据是否是商品详情行
items元素必须大等于3
若此算法判断通过则推荐使用get_good_302方法解析
实用举例:
Qty      Name        Subtotal     
*2       tu dou      10000
^4       tu dou      10000
"""


def is_good_302(items):
    if len(items) >= 3:
        qty = re.sub(const.REG_EXP_SPECIAL_CHAR, "", items[0])
        if utils.is_int_price(qty) and int(qty) < 100 \
                and isinstance(items[1], str) \
                and utils.can_to_number(items[len(items)-1]):
            return True
        else:
            return False
    else:
        return False


def get_good_302(items):
    if len(items) >= 3:
        qty = int(re.sub(const.REG_EXP_SPECIAL_CHAR, "", items[0]))
        name = " ".join(items[1:(len(items)-1)])
        subtotal = utils.parse_format_price(items[len(items) - 1])
        unit_price = subtotal / qty
        good = dict()
        good.setdefault(const.GOOD_NAME, name)
        good.setdefault(const.GOOD_QTY, qty)
        good.setdefault(const.GOOD_UNIT_PRICE, unit_price)
        good.setdefault(const.GOOD_SUBTOTAL, subtotal)
        return good

"""
判断该行数据是否是商品详情行
items元素必须大等于4
若此算法判断通过则推荐使用get_good_401方法解析
实用举例:
No     Name     Qty     Subtotal     
1      tu dou   *2      10000
2      tu dou   #3      10000.12
3      tu dou   ^4      10000
"""


def is_good_401(items):
    if len(items) >= 4:
        qty = re.sub(const.REG_EXP_SPECIAL_CHAR, "", items[len(items) - 2])
        if utils.is_int_price(items[0]) and int(items[0]) < 100 \
                and isinstance(items[1], str) \
                and utils.is_int_price(qty) and int(qty) < 100 \
                and utils.can_to_number(items[len(items)-1]) and float(items[len(items)-1]) > 100:
            return True
        else:
            return False
    else:
        return False


"""
判断该行数据是否是商品详情行
items元素必须大等于4
若此算法判断通过则推荐使用get_good_402方法解析
实用举例:
No     Name         unit_price  Subtotal
1      tu dou       10000       20000
2      tu dou       10000.12    30000.36
3      tu dou       10000       40000
"""


def is_good_402(items):
    if len(items) >= 4:
        if utils.is_int_price(items[0]) and int(items[0]) < 100 \
                and isinstance(items[1], str) \
                and utils.can_to_number(items[len(items)-2]) and float(items[len(items)-2]) > 100 \
                and utils.can_to_number(items[len(items)-1]) and float(items[len(items)-1]) > 100 \
                and (float(items[len(items)-1]))%(float(items[len(items)-2])) == 0:
            return True
        else:
            return False
    else:
        return False

"""
判断该行数据是否是商品详情行
items元素必须大等于4
若此算法判断通过则推荐使用get_good_403方法解析
实用举例:
Qty     Name         unit_price  Subtotal
1       tu dou       10000       20000
2       tu dou       10000.12    30000.36
1       tu dou       10000       40000
"""


def is_good_403(items):
    if len(items) >= 4:
        if utils.is_int_price(items[0]) and int(items[0]) < 100 \
                and isinstance(items[1], str) \
                and utils.can_to_number(items[len(items) - 2]) and utils.parse_format_price(items[len(items) - 2]) > 100 \
                and utils.can_to_number(items[len(items) - 1]) and utils.parse_format_price(items[len(items) - 1]) > 100 \
                and utils.parse_format_price(items[len(items) - 1]) % utils.parse_format_price(items[len(items) - 2]) == 0:
            return True
        else:
            return False
    else:
        return False


def get_good_403(items):
        qty = int(items[0])
        name = " ".join(items[1 : len(items)-3])
        unit_price = utils.parse_format_price(items[len(items)-2])
        subtotal = utils.parse_format_price(items[len(items)-1])
        good = dict()
        good.setdefault(const.GOOD_NAME, name)
        good.setdefault(const.GOOD_QTY, qty)
        good.setdefault(const.GOOD_UNIT_PRICE, unit_price)
        good.setdefault(const.GOOD_SUBTOTAL, subtotal)
        return good

