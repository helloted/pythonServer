# coding:utf-8

from reco.main import const

def get_parse_keys(serial_num):
    if serial_num == "6201001000001":
        return __get_parse_keys_6201001000001()
    elif serial_num == "6201001000002":
        return __get_parse_keys_6201001000001()
    elif serial_num == "6201001000003":
        return __get_parse_keys_6201001000001()
    elif serial_num == "6201001000004":
        return __get_parse_keys_6201001000001()
    elif serial_num == "6201001000005":
        return __get_parse_keys_6201001000001()
    

def __get_parse_keys_6201001000001():
    parse_key = dict()
    parse_key.setdefault(const.RECO_CMD_NO, 100)
    parse_key.setdefault(const.RECO_ORDER_KEYS, ["WOOYOO", "CAFE", "SUNTER"])
    parse_key.setdefault(const.RECO_TITLE_KEYS, ["WOOYOO", "CAFE", "SUNTER"])
    parse_key.setdefault(const.RECO_ID_KEYS, ["Invoice"])
    parse_key.setdefault(const.RECO_TIME_KEYS, ["Closed"])
    parse_key.setdefault(const.RECO_EMAIL_KEYS, ["Email"])
    parse_key.setdefault(const.RECO_MOBILE_PHONE_KEYS, ["SMS"])
    parse_key.setdefault(const.RECO_LANDLINE_PHONE_KEYS, ["SMS"])
    parse_key.setdefault(const.RECO_GOOD_NO, 302)
    parse_key.setdefault(const.RECO_SUBTOTAL_KEYS, ["Subtotal"])
    parse_key.setdefault(const.RECO_TAX_KEYS, ["Tax1"])
    parse_key.setdefault(const.RECO_TOTAL_KEYS, ["Total"])
    return parse_key