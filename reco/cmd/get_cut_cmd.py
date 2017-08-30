# coding:utf-8


def get_cmd(no):
    if no == 100:
        return get_cmd_100_1d56()
    elif no == 200:
        return get_cmd_200_1b6d()


def get_local_cut_cmd():
    return "1D 56 01"


"""
1d 56切刀指令集
走纸并切刀指令最多走纸15个纵向移动单位
"""


def get_cmd_100_1d56():
    cut_cmd_list = ["1D 56", "1D 56 00", "1D 56 01", "1D 56 48", "1D 56 49"]
    base = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F"]
    for i in range(len(base)):
        cut_cmd_list.append("1D 56 65 " + base[i])
        cut_cmd_list.append("1D 56 66 " + base[i])
    cut_cmd_list.reverse()
    return cut_cmd_list


"""
1B 6D切刀指令集
"""


def get_cmd_200_1b6d():
    cut_cmd_list = ["1B 6D", "1B 6D 00", "1B 6D 01", "1B 6D 48", "1B 6D 49", "1B 6D 0D"]
    base = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F"]
    for i in range(len(base)):
        cut_cmd_list.append("1B 6D 65 " + base[i])
        cut_cmd_list.append("1B 6D 66 " + base[i])
    cut_cmd_list.reverse()
    return cut_cmd_list

