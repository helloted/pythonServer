# coding:utf-8


import binascii
from reco.util import utils
from log_util.device_logger import logger
from reco.cmd import get_cut_cmd


from super_utils import deal_sn_handle


def gen_sn_and_qr(order):
    re_dict = deal_sn_handle.handel_sn(order.get("serial_num"))
    sn = re_dict.get("deal_sn")
    qr = re_dict.get("url")
    return [sn, qr]


def gen_qr_cmd(order):
    qr = order.get("qr")
    len_hex = hex(len(str(qr).decode("utf-8").encode("gb18030")) + 3)
    len_hex_str = str(len_hex).replace("0x", "")
    if len_hex_str.__len__() == 1:
        len_hex_str = "0"+len_hex_str

    hex_qr = utils.hex_add_blank(binascii.b2a_hex(qr))

    # 居中
    hex_1 = "1b 61 01"
    # 最后字节设置模块大小  级别  1 ≤ n ≤ 16                    （注释为10进制，代码中为16进制）
    hex_2 = "1d 28 6b 03 00 31 43 06"
    # 最后一字节选择纠错等级  48 49 50 51  对应  7% 15% 25% 30%   （注释为10进制，代码中为16进制）
    hex_3 = "1d 28 6b 03 00 31 45 30"
    # 存储qr（qr数据要紧跟此命令）
    hex_4 = "1d 28 6b " + len_hex_str + " 00 31 50 30"
    # 打印qr
    hex_5 = "1d 28 6b 03 00 31 51 30"
    # 走纸
    hex_6 = "0a 0a 0a 0a 0a 0a 0a 0a"

    return hex_1 + " " + hex_2 + " " + hex_3 + " " + hex_4 + " " + hex_qr + " " + hex_5 + " " + hex_6


"""
追加二维码或者切刀
result_item = ["切割后的指令item"， {订单}]
"""


def add_qr(serial_num, result):
    time_stamp = utils.get_millisecond()
    for i in range(len(result)):
        result_item = result[i]
        cmd_item = result_item[0]
        logo = result_item[1]
        order = result_item[2]
        if order is not None:
            logger.debug("  是订单 追加二维码...追加切刀...")
            # 检查时间戳
            t = order.get("time")
            if t is None or t == 0:
                t = time_stamp + i
            order["time"] = t
            # 生成sn 和 qr文本
            sn_qr = gen_sn_and_qr(order)
            order.setdefault("sn", sn_qr[0])
            order.setdefault("qr", sn_qr[1])
            # 追加qr指令
            cmd_item = cmd_item + " " + gen_qr_cmd(order)
            # 追加切刀
            cmd_item = cmd_item + " " + get_cut_cmd.get_local_cut_cmd()
            # 是否还原到居左对齐  justification
            cmd_item = set_justification(serial_num, cmd_item)

        else:
            logger.debug("不是订单,追加切刀")
            cmd_item = cmd_item + " " + get_cut_cmd.get_local_cut_cmd()
        result_item_dict = dict()
        result_item_dict.setdefault("order_data", cmd_item)
        result_item_dict.setdefault("logo_data", logo)
        result_item_dict.setdefault("order", order)
        result[i] = result_item_dict
    logger.debug("追加结束:")
    for r in result:
        logger.debug(r)
    return result


def set_justification(serial_num, cmd_item):
    if serial_num == '6201001000001':
        cmd_item = cmd_item + "1B 61 00 "
    elif serial_num == '6201001000004':
        cmd_item = cmd_item + "1B 61 00 "
    elif serial_num == '6201001000003':
        cmd_item = cmd_item + "1B 61 00 "
    return cmd_item

if __name__ == "__main__":
    print gen_qr_cmd("ffff")