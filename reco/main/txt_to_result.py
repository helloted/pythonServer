# coding:utf-8

import os
import re
import json
import const

from reco.handler import reco_good_line_handler
from reco.handler import reco_id_line_handler
from reco.handler import reco_tax_line_handler
from reco.handler import reco_total_line_handler
from reco.handler import reco_title_line_handler
from reco.handler import reco_contact_line_handler
from reco.handler import reco_time_line_handler
from reco.handler import parse_key_handler
from reco.handler import reco_subtotal_line_handler
from reco.util import utils
from log_util.device_logger import logger


class TxtToResult:
    def __init__(self, ori_data_dict):
        self.ori_data_dict = ori_data_dict

        _serial_num = ori_data_dict.get(const.RECO_SERIAL_NUM)
        _order_keys = ori_data_dict.get(const.RECO_ORDER_KEYS)
        _title_keys = ori_data_dict.get(const.RECO_TITLE_KEYS)
        _id_keys = ori_data_dict.get(const.RECO_ID_KEYS)
        _time_keys = ori_data_dict.get(const.RECO_TIME_KEYS)
        _email_keys = ori_data_dict.get(const.RECO_EMAIL_KEYS)
        _mobile_phone_keys = ori_data_dict.get(const.RECO_MOBILE_PHONE_KEYS)
        _landline_phone_keys = ori_data_dict.get(const.RECO_LANDLINE_PHONE_KEYS)
        _good_no = ori_data_dict.get(const.RECO_GOOD_NO)
        _subtotal_keys = ori_data_dict.get(const.RECO_SUBTOTAL_KEYS)
        _tax_keys = ori_data_dict.get(const.RECO_TAX_KEYS)
        _total_keys = ori_data_dict.get(const.RECO_TOTAL_KEYS)

        # 解析关键字
        self._serial_num = "" if _serial_num is None else _serial_num
        self._order_keys = [] if _order_keys is None else _order_keys.split("#")
        self._title_keys = [] if _title_keys is None else _title_keys.split("#")
        self._id_keys = [] if _id_keys is None else _id_keys.split("#")
        self._time_keys = [] if _time_keys is None else _time_keys.split("#")
        self._email_keys = [] if _email_keys is None else _email_keys.split("#")
        self._mobile_phone_keys = [] if _mobile_phone_keys is None else _mobile_phone_keys.split("#")
        self._landline_phone_keys = [] if _landline_phone_keys is None else _landline_phone_keys.split("#")
        self._good_no = 0 if _good_no is None else _good_no
        self._subtotal_keys = [] if _subtotal_keys is None else _subtotal_keys.split("#")
        self._tax_keys = [] if _tax_keys is None else _tax_keys.split("#")
        self._total_keys = [] if _total_keys is None else _total_keys.split("#")

        # 测试数据
        keys = parse_key_handler.get_parse_keys(self._serial_num)
        self._cmd_no = keys.get(const.RECO_CMD_NO)
        self._order_keys = keys.get(const.RECO_ORDER_KEYS)
        self._title_keys = keys.get(const.RECO_TITLE_KEYS)
        self._id_keys = keys.get(const.RECO_ID_KEYS)
        self._time_keys = keys.get(const.RECO_TIME_KEYS)
        self._email_keys = keys.get(const.RECO_EMAIL_KEYS)
        self._mobile_phone_keys = keys.get(const.RECO_MOBILE_PHONE_KEYS)
        self._landline_phone_keys = keys.get(const.RECO_LANDLINE_PHONE_KEYS)
        self._good_no = keys.get(const.RECO_GOOD_NO)
        self._subtotal_keys = keys.get(const.RECO_SUBTOTAL_KEYS)
        self._tax_keys = keys.get(const.RECO_TAX_KEYS)
        self._total_keys = keys.get(const.RECO_TOTAL_KEYS)

        # 0--商品第一列前  1--商品第一列后(包括第一列)
        self._step = 0

        # 存储解析结果
        self._order_dict = dict()
        self._good_list = list()

    def resolve(self, txt):
        # 判断是否为“结账单”
        is_order = True
        for key in self._order_keys:
           if key not in txt:
               is_order = False
        logger.debug("判断是否为结账单:")
        logger.debug(is_order)
        if is_order:
            pass
        else:
            return None

        # 逐行解析
        lines = txt.splitlines()
        for line in lines:
            self.reco_line(line)

        # 若没有解析到的字段设置默认值
        self._order_dict.setdefault(const.ORDER_SERIAL_NUM, self._serial_num)
        self._order_dict.setdefault(const.ORDER_ITEMS, self._good_list)
        self._order_dict.setdefault(const.ORDER_TITLE, None)
        self._order_dict.setdefault(const.ORDER_SHOP_NAME, None)
        self._order_dict.setdefault(const.ORDER_EMAIL, None)
        self._order_dict.setdefault(const.ORDER_MOBILE_PHONE, None)
        self._order_dict.setdefault(const.ORDER_LANDLINE_PHONE, None)
        self._order_dict.setdefault(const.ORDER_CASHIER, None)
        self._order_dict.setdefault(const.ORDER_ORDER_ID, None)
        self._order_dict.setdefault(const.ORDER_TIME, None)
        self._order_dict.setdefault(const.ORDER_TOTAL, None)
        self._order_dict.setdefault(const.ORDER_SUBTOTAL, None)
        self._order_dict.setdefault(const.ORDER_TAX, None)

        self._order_dict[const.ORDER_TIME] = utils.get_millisecond()

        return self._order_dict

    # 解析一行
    def reco_line(self, line):
        # 多空格变单空格
        new_line = re.sub(r"\s{2,}", " ", line).strip()
        # 按空格切割
        items = new_line.split(" ", len(new_line))
        # 单空格过滤
        if len(items) == 0 or (len(items) == 1 and len(items[0]) == " "):
            return

        # 判断是否解析到商品第一列
        if self._step == 0 and reco_good_line_handler.is_good_302(items):
            self._step = 1
            logger.debug("开始解析商品行")

        # 第一步 商品第一列前（不包括第一列）  step == 0
        if self._step == 0:
            # title
            if reco_title_line_handler.is_title(items, self._title_keys):
                title = reco_title_line_handler.get_title(items)
                self._order_dict.setdefault(const.ORDER_TITLE, title)
                return

            # email
            if reco_contact_line_handler.is_email(items, self._email_keys):
                email = reco_contact_line_handler.get_email(items)
                self._order_dict.setdefault(const.ORDER_EMAIL, email)
                return

            # mobile phone
            if reco_contact_line_handler.is_mobile_phone(items, self._mobile_phone_keys):
                mobile_phone = reco_contact_line_handler.get_mobile_phone(items)
                self._order_dict.setdefault(const.ORDER_MOBILE_PHONE, mobile_phone)
                return

            # landline phone
            if reco_contact_line_handler.is_landline_phone(items, self._landline_phone_keys):
                landline_phone = reco_contact_line_handler.get_landline_phone(items)
                self._order_dict.setdefault(const.ORDER_LANDLINE_PHONE, landline_phone)
                return

            # time
            if reco_time_line_handler.is_time(items, self._time_keys):
                time = reco_time_line_handler.get_time(items)
                self._order_dict.setdefault(const.ORDER_TIME, time)
                return

            # ID
            if reco_id_line_handler.is_id(items, self._id_keys):
                order_id = reco_id_line_handler.get_id(items, self._id_keys)
                self._order_dict.setdefault(const.ORDER_ORDER_ID, order_id)
                return

        # 第二步 商品第一列后（包括第一列）   step == 1
        elif self._step == 1:
            # good
            good = dict()

            if self._good_no == 0:
                pass
            elif self._good_no == 201:
                pass
            elif self._good_no == 202:
                pass
            elif self._good_no == 203:
                pass
            elif self._good_no == 301:
                pass
            elif self._good_no == 302:
                if reco_good_line_handler.is_good_302(items):
                    good = reco_good_line_handler.get_good_302(items)
            elif self._good_no == 303:
                pass
            elif self._good_no == 401:
                pass
            elif self._good_no == 402:
                pass
            elif self._good_no == 403:
                pass

            if good:
                name = good.get(const.GOOD_NAME)
                qty = good.get(const.GOOD_QTY)
                unit_price = good.get(const.GOOD_UNIT_PRICE)
                subtotal = good.get(const.GOOD_SUBTOTAL)
                item_good = {const.GOOD_NAME: name, const.GOOD_QTY: qty, const.GOOD_UNIT_PRICE: unit_price, const.GOOD_SUBTOTAL: subtotal}
                self._good_list.append(item_good)
                logger.debug(self._good_list)
                return

            # subtotal
            if reco_subtotal_line_handler.is_subtotal_line(items, self._subtotal_keys):
                subtotal = reco_subtotal_line_handler.get_subtotal(items)
                self._order_dict.setdefault(const.ORDER_SUBTOTAL, subtotal)
                return

            # tax
            if reco_tax_line_handler.is_tax_line(items, "Tax1"):
                tax = reco_tax_line_handler.get_tax(items)
                self._order_dict.setdefault(const.ORDER_TAX, tax)
                return

            # total
            if reco_total_line_handler.is_total_line(items, "Total"):
                total = reco_total_line_handler.get_total(items)
                self._order_dict.setdefault(const.ORDER_TOTAL, total)
                return

            # time
            if reco_time_line_handler.is_time(items, self._time_keys):
                time = reco_time_line_handler.get_time(items, self._time_keys)
                self._order_dict.setdefault(const.ORDER_TIME, time)
                return

if __name__ == "__main__":
    f = open(os.getcwd()+"/z_re.txt", "r")
    lines = f.readlines()
    txtToResult = TxtToResult()
    logger.debug(txtToResult.resolve(lines))

