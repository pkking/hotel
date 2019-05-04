#!/usr/bin/python
# -*- coding: UTF-8 -*-
import struct
from socket import *

import types


class SocketLibrary:
    """
    Python Test Library for Tcp Socket
    """

    def __init__(self):
        self.tcpTimeout = 1
        self.tcpSock = socket(AF_INET, SOCK_STREAM)

        self.tcpSock.setsockopt(SOL_SOCKET, SO_RCVTIMEO, struct.pack('LL', self.tcpTimeout, 0))
        self.tcpSock.settimeout(self.tcpTimeout)
        self.tcpSock.connect(('127.0.0.1', 5555))

    def SendCommand(self, cmdName, *args):
        """
        SendCommand commandString
        """
        cmd = cmdName
        for itemArgs in args:
            cmd = cmd + ' ' + str(itemArgs)

        self.tcpSock.send(cmd)

        data = self.tcpSock.recv(1024)
        data = data.strip()
        data = unicode(data, 'gbk').encode('utf8')

        # tcpSock.close()
        return data
