# coding:utf-8

from reco.util import utils

"""
判断该行数据是否是tax行
若此算法判断通过则推荐使用get_tax方法解析
@:param keyword 用于判断改行是否为tax行
实用举例:
Tax1                    30000
"""


def is_tax_line(items, keys):
    if len(items) >= 2:
        for key in keys:
            if key not in items:
                return False

        tax = utils.parse_format_price(items[len(items)-1])
        if type(tax) == int or type(tax) == float:
            return True
    return False


def get_tax(items):
    if len(items) == 2:
        subtotal = utils.parse_format_price(items[1])
        return subtotal
    return None


if __name__ == "__main__":
    print "开始"
    lst = ["TAx1", "999,,.99999"]
    print is_tax_line(lst, "tax1")
    print get_tax(lst)
    print "get_tax"
