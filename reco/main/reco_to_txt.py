# coding:utf-8

import json
import os

from reco.util import utils
from log_util.device_logger import logger


class RecoToTxt:
    def __init__(self, cmd):
        self.cmd = cmd
        self.whitespace = "\t"+"\n"+"\r"+"\f"+"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ";

    def parse(self, ori):
        inStr = ori.strip().upper()
        cnt = inStr.split(" ", len(inStr))

        cmd1 = json.loads(self.cmd)
        cmds = cmd1

        i = 0
        item = ""
        obj = ""
        re = ""
        while i < len(cnt):
            item = cnt[i]
            if item in cmds.keys():
                obj = cmds[item]
                if not isinstance(obj, int):
                    cmds = obj
                else:
                    i += int(obj)
                    cmds = cmd1
            elif cmds == cmd1:
                c = utils.hex_to_str(cnt[i])
                if self.whitespace.find(c) != -1:
                    re += c
            else:
                cmds = cmd1
                i -= 1
            i += 1
        return re


if __name__ == "__main__":

    f = open(os.getcwd()+"/z_capture_data.txt", "r")
    ori = f.read()
    logger.debug("源数据")
    logger.debug(ori)

    reco = RecoToTxt()
    re = reco.parse(ori)
    f = open(os.getcwd()+"/z_re.txt", "w")
    f.write(re)
    logger.debug("指令解析结束")
    logger.debug(re)

