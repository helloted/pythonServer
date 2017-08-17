# coding:utf-8
# 根据编号获取指令集
# 1xx--爱普生指令集

import json


def _get_cmd(no):
    if no == 100:
        return __get_cmd_100()


"""
ESC 指令集 编号100
"""


def __get_cmd_100():
    cmd_1b = dict()
    cmd_1b.setdefault("72", {"00": 0})
    cmd_1b.setdefault("56", 1)
    cmd_1b.setdefault("53", 0)
    cmd_1b.setdefault("54", 1)
    cmd_1b.setdefault("30", 3)
    cmd_1b.setdefault("2D", 1)
    cmd_1b.setdefault("0C", 0)
    cmd_1b.setdefault("63", {"33": 1, "34": 1, "35": 1})
    cmd_1b.setdefault("64", {"00": 0})
    cmd_1b.setdefault("65", 1)
    cmd_1b.setdefault("70", 3)
    cmd_1b.setdefault("20", 1)
    cmd_1b.setdefault("4D", 1)
    cmd_1b.setdefault("52", 1)
    cmd_1b.setdefault("3F", 1)
    cmd_1b.setdefault("5C", 2)
    cmd_1b.setdefault("3D", 1)
    cmd_1b.setdefault("24", 2)
    cmd_1b.setdefault("25", 1)
    cmd_1b.setdefault("26", 4)
    cmd_1b.setdefault("6D", 0)
    cmd_1b.setdefault("21", {"10": 0, "00": 0, "01": 0, "20": 0, "08": 0, "80": 0})
    cmd_1b.setdefault("61", {"00": 0})
    cmd_1b.setdefault("33", 1)
    cmd_1b.setdefault("32", 0)
    cmd_1b.setdefault("44", 2)
    cmd_1b.setdefault("45", {"00": 0})
    cmd_1b.setdefault("40", 0)
    cmd_1b.setdefault("4C", 0)
    cmd_1b.setdefault("74", 1)
    cmd_1b.setdefault("47", 1)
    cmd_1b.setdefault("7B", 1)
    cmd_1b.setdefault("4A", 1)
    cmd_1b.setdefault("57", 8)
    cmd_1b.setdefault("2A", 4)

    cmd_1c = dict()
    cmd_1c.setdefault("2D", 1)
    cmd_1c.setdefault("26", 1)
    cmd_1c.setdefault("21", 1)
    cmd_1c.setdefault("71", 1)
    cmd_1c.setdefault("70", 2)
    cmd_1c.setdefault("32", 3)
    cmd_1c.setdefault("57", 1)
    cmd_1c.setdefault("52", 2)

    cmd_1d = dict()
    cmd_1d.setdefault("24", 2)
    cmd_1d.setdefault("6B", 3)
    cmd_1d.setdefault("21", 1)
    cmd_1d.setdefault("48", 1)
    cmd_1d.setdefault("76", {"30": 6})
    cmd_1d.setdefault("42", 1)
    cmd_1d.setdefault("57", 2)
    cmd_1d.setdefault("56", 1)
    cmd_1d.setdefault("28", {"6B": 5, "41": 4})
    cmd_1d.setdefault("50", 2)
    cmd_1d.setdefault("77", 1)
    cmd_1d.setdefault("61", 1)
    cmd_1d.setdefault("2F", 1)
    cmd_1d.setdefault("2A", 3)
    cmd_1d.setdefault("66", 1)
    cmd_1d.setdefault("68", 1)
    cmd_1d.setdefault("5E", 3)
    cmd_1d.setdefault("3A", 0)
    cmd_1d.setdefault("4C", 2)
    cmd_1d.setdefault("5C", 2)
    cmd_1d.setdefault("72", 1)

    cmd = dict()
    cmd.setdefault("1B", cmd_1b)
    cmd.setdefault("1C", cmd_1c)
    cmd.setdefault("1D", cmd_1d)
    return json.dumps(cmd)

if __name__ == "__main__":


   print __get_cmd_100()
