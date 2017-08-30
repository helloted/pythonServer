# coding:utf-8

from reco.util import utils
from reco.main import const

flag_char = ["+", "-", "*", "/", "#"]


"""
如果此条件判断通过，建议使用相同编号方法获取结果

1 Honey Black Tea  20,000     20,000

      name              unit_price      total_price 
      + +Coffee Jelly   3,000           3,000
      + +Pudding        4,000           4,000
      + +Purple Rice    4,000           4,000
      + +QQ             4,000           4,000
"""


def is_subgood_301(items):
    if len(items) >= 3:
        name = " ".join(items[0 : len(items)-2])
        unit_price = utils.parse_format_price(items[len(items)-2])
        total_price = utils.parse_format_price(items[len(items)-1])

        has_flag = False
        for c in flag_char:
            if name.startswith(c):
                has_flag = True
                break
        if has_flag and unit_price is not None and total_price is not None:
                return True


def get_subgood_301(items):
    name = " ".join(items[0: len(items) - 2])
    for c in flag_char:
        name = name.replace(c, "")
    unit_price = utils.parse_format_price(items[len(items) - 2])
    total_price = utils.parse_format_price(items[len(items) - 1])
    if total_price != 0 and unit_price != 0:
        qty = int(total_price / unit_price)
    else:
        qty = 1

    subgood = dict()
    subgood.setdefault(const.SUBGOOD_NAME, name)
    subgood.setdefault(const.SUBGOOD_QTY, qty)
    subgood.setdefault(const.SUBGOOD_UNIT_PRICE, unit_price)
    subgood.setdefault(const.SUBGOOD_TOTAL_PRICE, total_price)
    return subgood


