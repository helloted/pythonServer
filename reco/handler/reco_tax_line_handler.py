# coding:utf-8

from reco.util import utils

"""
判断该行数据是否是tax行
若此算法判断通过则推荐使用get_tax方法解析
@:param keyword 用于判断改行是否为tax行
实用举例:
Tax1                    30000
"""


def is_tax_line(items, keyword):
    if keyword is None or len(keyword) == 0:
        keyword == "Tax1"
    keyword = keyword.lower()
    if len(items) == 2:
        items0 = str(items[0]).lower()
        items1 = utils.parse_format_price(items[1])
        if type(items0) == str and keyword in items0 \
                and (type(items1) == int or type(items1) == float) and items1 > 100:
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
