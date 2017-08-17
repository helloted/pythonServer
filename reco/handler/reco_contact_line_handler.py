# coding:utf-8

import re

from reco.main import const


"""
判断该行是否为订单email行
判断通过条件:所有key必须同时存在于该行
             且符合email正则表达式
"""


def is_email(items, keys):
    has_key = False
    if list(keys).__len__() > 0:
        has_key = True

    is_all_in = True
    for key in keys:
        if key not in items:
            is_all_in = False

    is_valid_email = True
    pattern = re.compile(const.REG_EXP_EMAIL)
    for item in items:
        search = pattern.search(item)
        if search:
            is_valid_email = True

    return has_key and is_all_in and is_valid_email


"""
解析出订单email
"""


def get_email(items):
    pattern = re.compile(const.REG_EXP_EMAIL)
    for item in items:
        search = pattern.search(item)
        if search:
            return search.group()


"""
判断该行是否为订单手机号码行
判断通过条件:所有key必须同时存在于该行
             且符合手机正则表达式（正规手机号码:"08xx xxxx xxxx",08开头共11位，或者8开头共10位）
"""


def is_mobile_phone(items, keys):
    has_key = False
    if list(keys).__len__() > 0:
        has_key = True

    is_all_in = True
    for key in keys:
        if key not in items:
            is_all_in = False

    is_valid_mobile_pbone = False
    pattern = re.compile(const.REG_EXP_MOBILE_PHONE)
    search = pattern.search("".join(items))
    if search:
        is_valid_mobile_pbone = True

    return has_key and is_all_in and is_valid_mobile_pbone


def get_mobile_phone(items):
    pattern = re.compile(const.REG_EXP_MOBILE_PHONE)
    line = re.sub(r"-|\+", "", "".join(items))
    search = pattern.search(line)
    if search:
        return search.group()


"""
判断该行是否为订单座机号码行
判断通过条件:所有key必须同时存在于该行
             且符合座机正则表达式（正规手机号码:"08xx xxxx xxxx",08开头共11位，或者8开头共10位）
"""


def is_landline_phone(items, keys):
    has_key = False
    if list(keys).__len__() > 0:
        has_key = True

    is_all_in = True
    for key in keys:
        if key not in items:
            is_all_in = False

    is_valid_mobile_pbone = False
    pattern = re.compile(const.REG_EXP_MOBILE_PHONE)
    search = pattern.search("".join(items))
    if search:
        is_valid_mobile_pbone = True

    return has_key and is_all_in and is_valid_mobile_pbone


def get_landline_phone(items):
    pattern = re.compile(const.REG_EXP_MOBILE_PHONE)
    line = re.sub(r"-|\+", "", "".join(items))
    search = pattern.search(line)
    if search:
        return search.group()

