#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import os
import sys

import SocketLibrary

com = SocketLibrary.SocketLibrary()

logfile = os.path.join(os.path.dirname(__file__), 'result.log')

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
handler = logging.FileHandler(logfile, 'a')
logging.root.addHandler(handler)


# 自定义的AW请写作这个文件中

def send_cmd(cmd):
    return com.SendCommand(cmd)
