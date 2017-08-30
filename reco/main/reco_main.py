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
    | cut_cmd_no         | 0                         |
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
    | subgood_no         | 302                       |
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
        _cut_cmd_no = ori_data_dict.get(const.RECO_CUT_CMD_NO)
        _capture_data = ori_data_dict.get(const.RECO_CAPTURE_DATA)

        self._cmd_no = 0 if _cmd_no is None else _cmd_no
        self._cut_cmd_no = 0 if _cut_cmd_no is None else _cut_cmd_no
        self._capture_data = "" if _capture_data is None else str(_capture_data).upper()
        self._capture_data = utils.hex_add_blank(self._capture_data)

        # 测试数据
        keys = parse_key_handler.get_parse_keys(_serial_num)
        self._serial_num = _serial_num
        self._cmd_no = keys.get(const.RECO_CMD_NO)
        self._cut_cmd_no = keys.get(const.RECO_CUT_CMD_NO)

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
            result_reco = self._start_reco(self._capture_data)

            # result_qr
            result_qr = qr_handler.add_qr(self._serial_num, result_reco)

            # 去除hex中的空白字符
            result_remove_blank_char = self._remove_blank_char(result_qr)

            # 检查id是否重复，以此判断此单是否有效的一个条件
            result_check_id_repeat = self._check_id_repeat(result_remove_blank_char)

            # 判断订单是否解析成功以及每个订单是否有效
            result_add_status = self._check_reco_status(result_check_id_repeat)

            logger.debug("===================================================================================================================")
            logger.debug("        PARSE END    {'status'= true, 'order_list'=[{'logo_data'=None', 'order_data'=None, 'order'=order}, ]}      ")
            logger.debug("===================================================================================================================")

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
        cut_cmd_list = get_cut_cmd.get_cmd(self._cut_cmd_no)
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
            status_1, status_2 = True, True
            if order is None:
                status_1 = status_2 = status = False
            else:
                if order.get(const.ORDER_IS_ORDER) is False:
                    status_2 = False
            status_item = status_1 and status_2
            if status_item:
                status = True
                break
        result_add_status = {}
        result_add_status.setdefault("status", status)
        result_add_status.setdefault("order_list", result)
        return result_add_status

    # 判断每个订单是否有效
    # 此订单无效条件:
    # 1.如果is_order字段为False,则is_valid_order字段也为false
    # 2.id本次解析出的多个订单重复，默认第一个订单id有效
    # 3.id数据库查询历史，对比是否有重复
    def _check_id_repeat(self, result):
        logger.debug("判断每个订单是否有效，此处判断id重复")
        order_ids = [None]*len(result)
        for i in range(len(result)):
            result_item = result[i]
            order_temp = result_item.get("order")
            if order_temp is not None:
                order_id_temp = order_temp.get(const.ORDER_ORDER_ID)
                order_ids[i] = order_id_temp
            else:
                order_ids[i] = None
        logger.debug("order_ids:")
        logger.debug(order_ids)

        for i in range(len(result)):
            result_item = result[i]
            order = result_item.get("order")
            if order is not None:
                is_valid_order = order.get(const.ORDER_IS_VALID_ORDER)
                is_order = order.get(const.ORDER_IS_ORDER)
                order_id = order.get(const.ORDER_ORDER_ID)

                if is_valid_order is not None and is_valid_order is False:
                    pass
                elif is_order and (order_id is not None or order_id != ''):
                    if order_ids.count(order_id) == 1:
                        order[const.ORDER_IS_VALID_ORDER] = True
                    else:
                        if i == 0:
                            order[const.ORDER_IS_VALID_ORDER] = True
                        else:
                            order[const.ORDER_IS_VALID_ORDER] = False
                else:
                    order[const.ORDER_IS_VALID_ORDER] = False

        return result


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
    d = """{"cmd_no":100,"time_keys":"","order_keys":"","contact_keys":"","serial_num":"6201001000001","capture_data":"1D2F00010A1B210020202020202020202020202020202020434F4D454255590A202020202020202054484520504C415A412053454D414E474749204746203336350A202020202020202020202054454C502E203032312D33363037333333330A0A4E6F2E20537472756B202020203A20434250532D303030303036393733322F46460A54676C20537472756B202020203A2032302D4175672D323031372031373A35363A34350A4B617373612F4F7264657223203A2031202F2035202D200A50656C6179616E2F4B617369723A2041646D696E6973747261202F20414C490A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A202020203120486F6E657920426C61636B20546561202032302C303030202020202032302C3030300A2020202020202B202B436F66666565204A656C6C79202020332C303030202020202020332C3030300A2020202020202B202B50756464696E672020202020202020342C303030202020202020342C3030300A2020202020202B202B507572706C65205269636520202020342C303030202020202020342C3030300A2020202020202B202B515120202020202020202020202020342C303030202020202020342C3030300A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A4772616E64546F74616C203A2020202020202020202020202020202020202020202033352C3030300A42617961722020202020203A20202020202020202020202020202020202020312C3030302C3030300A20204361736820202020203A202020312C3030302C3030300A4B656D62616C69616E20203A2020202020202020202020202020202020202020203936352C3030300A0A20202020546572696D61206B617369682061746173206B756E6A756E67616E20616E64610A2020202020204861726761207375646168207465726D73756B2070616A616B205042310A0A0A0A0A0A0A0A0A1B6D1B21101B2120416E747269616E203A20351B21011B21000A0A1B21101B212051747920202020203A20311B21011B21000A0A434250532D303030303036393733322F46462032302D4175672D323031372031373A35363A34350A0A0A0A0A0A0A0A1B6D0D0A","subtotal_keys":"","good_no":302,"total_keys":"","tax_keys":"","id_keys":""}"""
    d = """{"cmd_no":100,"time_keys":"","order_keys":"","contact_keys":"","serial_num":"6201001000001","capture_data":"1D2F00010A1B210020202020202020202020202020202020434F4D454255590A202020202020202054484520504C415A412053454D414E474749204746203336350A202020202020202020202054454C502E203032312D33363037333333330A0A4E6F2E20537472756B202020203A20434250532D303030303036393733322F46460A54676C20537472756B202020203A2032302D4175672D323031372031373A35363A34350A4B617373612F4F7264657223203A2031202F2035202D200A50656C6179616E2F4B617369723A2041646D696E6973747261202F20414C490A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A202020203120486F6E657920426C61636B20546561202032302C303030202020202032302C3030300A2020202020202B202B436F66666565204A656C6C79202020332C303030202020202020332C3030300A2020202020202B202B50756464696E672020202020202020342C303030202020202020342C3030300A2020202020202B202B507572706C65205269636520202020342C303030202020202020342C3030300A2020202020202B202B515120202020202020202020202020342C303030202020202020342C3030300A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A4772616E64546F74616C203A2020202020202020202020202020202020202020202033352C3030300A42617961722020202020203A20202020202020202020202020202020202020312C3030302C3030300A20204361736820202020203A202020312C3030302C3030300A4B656D62616C69616E20203A2020202020202020202020202020202020202020203936352C3030300A0A20202020546572696D61206B617369682061746173206B756E6A756E67616E20616E64610A2020202020204861726761207375646168207465726D73756B2070616A616B205042310A0A0A0A0A0A0A0A0A1B6D1B21101B2120416E747269616E203A20351B21011B21000A0A1B21101B212051747920202020203A20311B21011B21000A0A434250532D303030303036393733322F46462032302D4175672D323031372031373A35363A34350A0A0A0A0A0A0A0A1B6D0D0A1D2F00010A1B210020202020202020202020202020202020434F4D454255590A202020202020202054484520504C415A412053454D414E474749204746203336350A202020202020202020202054454C502E203032312D33363037333333330A0A4E6F2E20537472756B202020203A20434250532D303030303036393733322F46460A54676C20537472756B202020203A2032302D4175672D323031372031373A35363A34350A4B617373612F4F7264657223203A2031202F2035202D200A50656C6179616E2F4B617369723A2041646D696E6973747261202F20414C490A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A202020203120486F6E657920426C61636B20546561202032302C303030202020202032302C3030300A2020202020202B202B436F66666565204A656C6C79202020332C303030202020202020332C3030300A2020202020202B202B50756464696E672020202020202020342C303030202020202020342C3030300A2020202020202B202B507572706C65205269636520202020342C303030202020202020342C3030300A2020202020202B202B515120202020202020202020202020342C303030202020202020342C3030300A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A4772616E64546F74616C203A2020202020202020202020202020202020202020202033352C3030300A42617961722020202020203A20202020202020202020202020202020202020312C3030302C3030300A20204361736820202020203A202020312C3030302C3030300A4B656D62616C69616E20203A2020202020202020202020202020202020202020203936352C3030300A0A20202020546572696D61206B617369682061746173206B756E6A756E67616E20616E64610A2020202020204861726761207375646168207465726D73756B2070616A616B205042310A0A0A0A0A0A0A0A0A1B6D1B21101B2120416E747269616E203A20351B21011B21000A0A1B21101B212051747920202020203A20311B21011B21000A0A434250532D303030303036393733322F46462032302D4175672D323031372031373A35363A34350A0A0A0A0A0A0A0A1B6D0D0A","subtotal_keys":"","good_no":302,"total_keys":"","tax_keys":"","id_keys":""}"""
    d = """{"cmd_no":100,"time_keys":"","order_keys":"","contact_keys":"","serial_num":"6201001000001","capture_data":"2020202020202020434F4D454255590A20202020202043454E5452414C205041524B204D414C4C204C542031202D203133310A202020202020202020202020544C50203038353130363037313131310A0A2A2A2A2052657072696E74202A2A2A200A4E6F2E20537472756B202020203A20434243502D303030303236353138312F46460A54676C20537472756B202020203A2032372D4175672D323031372032313A32393A34300A4B617373612F4F7264657223203A2031202F20323934202D200A50656C6179616E2F4B617369723A2041646D696E6973747261202F204B4152494E410A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A2020202031205461726F204D696C6B205465612020202032342C303030202020202032342C3030300A2020202020202B202B427562626C65202020202020202020332C303030202020202020332C3030300A2020202020202B20496365204C6573732020202020202020202020203020202020202020202020300A2020202020202B20532D3330252020202020202020202020202020203020202020202020202020300A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A4772616E64546F74616C203A2020202020202020202020202020202020202020202032372C3030300A42617961722020202020203A2020202020202020202020202020202020202020202032372C3030300A20204361736820202020203A20202020202032372C3030300A4B656D62616C69616E20203A202020202020202020202020202020202020202020202020202020300A0A20202020546572696D61206B617369682061746173206B756E6A756E67616E20616E64610A2020202020204861726761207375646168207465726D73756B2070616A616B205042310A0A0A0A0A0A0A1B6D1B21101B2120416E747269616E203A203239341B21011B21000A0A1B21101B212051747920202020203A20311B21011B21000A0A434243502D303030303236353138312F46462032372D4175672D323031372032313A32393A34300A0A0A0A0A0A1B6D0D0A","subtotal_keys":"","good_no":302,"total_keys":"","tax_keys":"","id_keys":""}"""
    d = """{"cmd_no":100,"time_keys":"","order_keys":"","contact_keys":"","serial_num":"6201001000004","capture_data":"2020202020202020434F4D454255590A20202020202043454E5452414C205041524B204D414C4C204C542031202D203133310A202020202020202020202020544C50203038353130363037313131310A0A2A2A2A2052657072696E74202A2A2A200A4E6F2E20537472756B202020203A20434243502D303030303236353138312F46460A54676C20537472756B202020203A2032372D4175672D323031372032313A32393A34300A4B617373612F4F7264657223203A2031202F20323934202D200A50656C6179616E2F4B617369723A2041646D696E6973747261202F204B4152494E410A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A2020202031205461726F204D696C6B205465612020202032342C303030202020202032342C3030300A2020202020202B202B427562626C65202020202020202020332C303030202020202020332C3030300A2020202020202B20496365204C6573732020202020202020202020203020202020202020202020300A2020202020202B20532D3330252020202020202020202020202020203020202020202020202020300A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A4772616E64546F74616C203A2020202020202020202020202020202020202020202032372C3030300A42617961722020202020203A2020202020202020202020202020202020202020202032372C3030300A20204361736820202020203A20202020202032372C3030300A4B656D62616C69616E20203A202020202020202020202020202020202020202020202020202020300A0A20202020546572696D61206B617369682061746173206B756E6A756E67616E20616E64610A2020202020204861726761207375646168207465726D73756B2070616A616B205042310A0A0A0A0A0A0A1B6D1B21101B2120416E747269616E203A203239341B21011B21000A0A1B21101B212051747920202020203A20311B21011B21000A0A434243502D303030303236353138312F46462032372D4175672D323031372032313A32393A34300A0A0A0A0A0A1B6D0D0A","subtotal_keys":"","good_no":302,"total_keys":"","tax_keys":"","id_keys":""}"""
    _reco_main = RecoMain(eval(d))
    _reco_main.parse()



