# coding:utf-8
# 本模块是根据传入的指令集编号获取对应的图片打印指令


"""
@:param cmd_no   指令集编号
@:param cmd_list 捕获的每单数据hex值的list
"""


def get_logo_data(cmd_no, data_list):
    if cmd_no == 100:
        return __get_logo_data_100(data_list)


"""
切割出数据中的图片数据
只切割出顺序第一个图片数据
返回 图片数据str
"""


def __get_logo_data_100(data_item):
    data_list = str(data_item).split(" ")
    for i in range(len(data_list)):
        if i+7 < len(data_list) and data_list[i] == "1D" and data_list[i+1] == "76" and data_list[i+2] == "30":
            xl = int(data_list[i+4])
            xh = int(data_list[i+5])
            yl = int(data_list[i+6])
            yh = int(data_list[i+7])
            logo_data_len = (xl + xh * 256) * (yl + yh * 256)
            logo_last_index = i+7+logo_data_len
            if logo_last_index < len(data_list):
                # data_list_1 = data_list[0:i]
                data_list_2 = data_list[i:logo_last_index+1]
                # data_list_3 = data_list[logo_last_index+1:len(data_list)]
                if data_list_2 is not None:
                    data_txt = " ".join(data_list_2)
                    return data_txt


if __name__ == "__main__":
    pass
    par = ["0A", "1D", "76", "30", "01", "02", "00", "02", "00", "0A", "0A", "0A", "0A", "xx"]
    print __get_logo_data_100(par)
    print par






