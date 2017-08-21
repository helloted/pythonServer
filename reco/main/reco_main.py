# coding:utf-8

import os
import re
import json
import traceback

import reco_to_txt
import txt_to_result
from reco.cmd import get_cmd
from reco.cmd import get_cut_cmd
from reco.cmd import get_logo_data
from reco.handler import qr_handler
from reco.util import utils
from log_util.device_logger import logger
from reco.main import const
from reco.handler import parse_key_handler

class RecoMain:

    """
    构造方法参数为字典:    keys中不能有空格不能有特殊字符
    +--------------------+---------------------------+
    | Key                | Value                     |
    +====================+===========================+
    | serial_num         | 6201001000001             |
    +--------------------+---------------------------+
    | cmd_no             | 0                         |
    +--------------------+---------------------------+
    | order_keys         | ["结账单", "账单"]        |
    +--------------------+---------------------------+
    | id_keys            | ["id", "No"]              |
    +--------------------+---------------------------+
    | time_keys          | ["time", "Date"]          |
    +--------------------+---------------------------+
    | contact_keys       | ["phone", "SMS"]          |
    +--------------------+---------------------------+
    | good_no            | 401                       |
    +--------------------+---------------------------+
    | subtotal_keys      | ["subtotal", "sub"]       |
    +--------------------+---------------------------+
    | tax_keys           | ["tax", "PB1"]            |
    +--------------------+---------------------------+
    | total_keys         | ["total", "Amount"]       |
    +--------------------+---------------------------+
    | capture_data       | "1C 70  .. .."            |
    +--------------------+---------------------------+
    """

    def __init__(self, ori_data_dict):
        self.ori_data_dict = ori_data_dict

        _serial_num = ori_data_dict.get(const.RECO_SERIAL_NUM)
        _cmd_no = ori_data_dict.get(const.RECO_CMD_NO)
        _capture_data = ori_data_dict.get(const.RECO_CAPTURE_DATA)

        self._cmd_no = 0 if _cmd_no is None else _cmd_no
        self._capture_data = "" if _capture_data is None else str(_capture_data).upper()
        self._capture_data = utils.hex_add_blank(self._capture_data)

        # 测试数据
        keys = parse_key_handler.get_parse_keys(_serial_num)
        self._cmd_no = keys.get(const.RECO_CMD_NO)

    """
    解析入口
    """
    def parse(self):
        try:
            logger.debug("=========================")
            logger.debug("       PARSE START       ")
            logger.debug("=========================")
            logger.debug("\n")

            # result
            result = self._start_reco(self._capture_data)

            # result_qr
            result_qr = qr_handler.add_qr(result)

            # 去除hex中的空白字符
            result_remove_blank_char = self._remove_blank_char(result_qr)

            # 判断订单是否解析成功
            result_add_status = self._check_reco_status(result_remove_blank_char)

            logger.debug("=====================================================================================================")
            logger.debug("        PARSE END    {'status'= true, 'result'=[{'cmd'='cmd', 'logo'='logo', 'order'=order}, ]}      ")
            logger.debug("=====================================================================================================")

            logger.debug("返回的数据:")
            logger.debug(result_add_status)
            return result_add_status
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error("解析异常,返回None")
            return None

    """
    循环解析订单
    @:param result = [[每单数据str, 此单中logo数据str, 订单dict],]
    """
    def _start_reco(self, capture_data):
        data_list = self._split_by_cut(capture_data)
        result = list()
        for data_item in data_list:
            logger.debug("开始解析此订单数据:")
            logger.debug(data_item)
            logger.debug("切割图片 ......")
            logo_txt = get_logo_data.get_logo_data(self._cmd_no, data_item)

            logger.debug("指令解析开始 ......")
            _reco_cmd = reco_to_txt.RecoToTxt(get_cmd._get_cmd(self._cmd_no))
            txt = _reco_cmd.parse(data_item)
            # with open(os.getcwd() + "/z_result.txt", "w") as f:
            #     f.write(txt)
            #     f.close()
            logger.debug("指令解析结束:")
            logger.debug(txt)

            logger.debug("文本解析开始 ......")
            _reco_txt = txt_to_result.TxtToResult(self.ori_data_dict)
            order = _reco_txt.resolve(txt)
            logger.debug("文本解析结束:")
            logger.debug(order)

            result_item = [data_item, logo_txt, order]
            result.append(result_item)
        logger.debug("此数据解析全部结束:")
        for temp in result:
            logger.debug(temp)
        return result

    """
    按切刀切割原始字符串
    """
    def _split_by_cut(self, ori_cmd):
        logger.debug("源数据")
        logger.debug(ori_cmd)
        cut_re = ""
        cut_cmd_list = get_cut_cmd.get_cmd(self._cmd_no)
        for cmd in cut_cmd_list:
            cut_re += (cmd+"|")
        cmd_list = re.split(cut_re, ori_cmd)
        for i in range(len(cmd_list)):
            ori_cmd_item = cmd_list[i]
            new_cmd_item = ori_cmd_item.strip(" ")
            if len(new_cmd_item) == 0:
                del cmd_list[i]
            else:
                cmd_list[i] = new_cmd_item
        logger.debug("切割后数据")
        for temp1 in cmd_list:
            logger.debug(temp1)
        logger.debug("去掉全部是0A的数据 ...")
        for temp2 in cmd_list:
            flag = True  # true--全部hex都是“0A”
            for hex_unit in temp2.split(" "):
                if hex_unit != "0A":
                    flag = False
            if flag:
                cmd_list.remove(temp2)
        logger.debug("去掉0A结果")
        for temp3 in cmd_list:
            logger.debug(temp3)
        return cmd_list

    # 移除 logo 和 订单指令中的空白字符
    def _remove_blank_char(self, result_qr):
        result_remove_blank = []
        for i in range(len(result_qr)):
            result_item = result_qr[i]
            order_data = result_item.get("order_data")
            logo_data = result_item.get("logo_data")
            order = result_item.get("order")
            if order_data is not None:
                order_data = utils.hex_remove_blank(order_data)
            if logo_data is not None:
                logo_data = utils.hex_remove_blank(logo_data)
            result_item_new = {}
            result_item_new.setdefault("order_data", order_data)
            result_item_new.setdefault("logo_data", logo_data)
            result_item_new.setdefault("order", order)
            result_remove_blank.append(result_item_new)
        return result_remove_blank

    # 判断解析结果是否成功
    # 1. 3个条件同时成立则某一订单解析成功为订单
    # 2. 多段数据只要有一个成功解析为订单则当前解析成功
    def _check_reco_status(self, result):
        logger.debug("判断是否成功解析")
        status = False
        for i in range(len(result)):
            result_item = result[i]
            order = result_item.get("order")
            status_1, status_2, status_3 = True, True, True
            if order is None:
                status_1 = status_2 = status = False
            else:
                if order.get(const.ORDER_TOTAL) is None or (order.get(const.ORDER_TOTAL) == 0):
                    status_2 = False
                if order.get(const.ORDER_ITEMS is None or (len(order.get(const.ORDER_ITEMS)) == 0)):
                    status_3 = False
            status_item = status_1 and status_2 and status_3
            if status_item:
                status = True
                break
        result_add_status = {}
        result_add_status.setdefault("status", status)
        result_add_status.setdefault("order_list", result)
        return result_add_status

if __name__ == "__main__":

    f = open(os.getcwd()+"/z_capture_data_logo.txt")
    lines = f.readlines()
    f.close()
    capture_data = " ".join(lines)

    ori_data_dict = dict()
    ori_data_dict.setdefault(const.RECO_SERIAL_NUM, "6201001000002")
    ori_data_dict.setdefault(const.RECO_CMD_NO, 100)
    ori_data_dict.setdefault(const.RECO_ORDER_KEYS, "WOOYOO#CAFE#SUNTER")
    ori_data_dict.setdefault(const.RECO_TIME_KEYS, "WOOYOO#CAFE#SUNTER")
    ori_data_dict.setdefault(const.RECO_ID_KEYS, "Ticket No")
    ori_data_dict.setdefault(const.RECO_TIME_KEYS, "Closed")
    ori_data_dict.setdefault(const.RECO_EMAIL_KEYS, "Email")
    ori_data_dict.setdefault(const.RECO_MOBILE_PHONE_KEYS, "SMS")
    ori_data_dict.setdefault(const.RECO_LANDLINE_PHONE_KEYS, "SMS")
    ori_data_dict.setdefault(const.RECO_GOOD_NO, 302)
    ori_data_dict.setdefault(const.RECO_SUBTOTAL_KEYS, "Total")
    ori_data_dict.setdefault(const.RECO_TAX_KEYS, "Tax1")
    ori_data_dict.setdefault(const.RECO_TOTAL_KEYS, "Total")
    ori_data_dict.setdefault(const.RECO_CAPTURE_DATA, capture_data)

    # 自定义数据测试
    # _reco_main = RecoMain(json.dumps(ori_data_dict))
    # _reco_main.parse()

    # 真实数据测试
    d = """{"capture_data":{"cmd_no":100,"time_keys":"","order_keys":"","contact_keys":"","serial_num":"6201001000002","capture_data":"1D21012020202020202020202020202020202020205469636B65742020202020202020202020202020202020200A1D2100446174653A31392F382F32303137202020202020202020202020202020202020202020202020202020200A1D210054696D653A31303A333320202020202020202020202020202020202020202020202020202020202020200A1D21005461626C653A2042313320202020202020202020202020202020202020202020202020202020202020200A1D21005469636B6574204E6F3A33332020202020202020202020202020202020202020202020202020202020200A1D21002D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A1D21002D203620546F617374656420426167656C204368656573652020202020202020202020202031332E35300A1D21003D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D0A1B47011D2101546F74616C3A2020202020202020202020202020202020202020202020202020202020202031332E35300A1D21004361736820202020202020202020202020202020202020202020202020202020202020202031332E35300A1B47001D21003D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D3D0A1D2101202020202020202020202020202020205468616E6B20596F7520202020202020202020202020202020200A1B64011D564200","subtotal_keys":"","good_no":302,"total_keys":"","tax_keys":"","id_keys":""},"upload_token":"87808cfc255972b725aa8c755605e3a2"}"""
    _reco_main = RecoMain(eval(d))
    _reco_main.parse()



