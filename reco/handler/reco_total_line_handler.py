# coding:utf-8

from reco.util import utils

"""
判断该行数据是否是total行
若此算法判断通过则推荐使用get_total方法解析
@:param keyword 用于判断改行是否为total行
实用举例:
Total                    30000
Total      :             30000
--  Total                30000
"""


def is_total_line(items, keys):
    if len(items) >= 2:
        for key in keys:
            if key not in items:
                return False

        price = utils.parse_format_price(items[len(items)-1])
        if type(price) == int or type(price) == float:
            return True
    return False


def get_total(items):
    return utils.parse_format_price(items[len(items)-1])


if __name__ == "__main__":
    print "开始"
    lst = ["Total", ":", "999,,.99999"]
    print is_total_line(lst, ["Total"])
    print get_total(lst)
    print "结束"
