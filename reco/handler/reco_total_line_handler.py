# coding:utf-8

from reco.util import utils

"""
判断该行数据是否是total行
若此算法判断通过则推荐使用get_total方法解析
@:param keyword 用于判断改行是否为total行
实用举例:
Total                    30000
"""


def is_total_line(items, keyword):
    if keyword is None or len(keyword) == 0:
        keyword == "total"
    keyword = keyword.lower()
    if len(items) == 2:
        items[1].replace(":","").replace(".","")
        items0 = str(items[0]).lower()
        items1 = utils.parse_format_price(items[1])
        if type(items0) == str and keyword in items0 \
                and (type(items1) == int or type(items1) == float) and items1 > 1:
            return True
    return False


def get_total(items):
    if len(items) == 2:
        subtotal = utils.parse_format_price(items[1])
        return subtotal
    return None


if __name__ == "__main__":
    print "开始"
    lst = ["Total", "999,,.99999"]
    print is_total_line(lst, "total")
    print get_total(lst)
    print "结束"
