# -*- coding: utf-8 -*-
"""
说明：考试工程文件，清不要修改该文件
      使用方法请阅读“python考试工程补充说明”
"""

import sys
import socket
import constants
from demo import OrderHotelSystem

# 该函数为考试工程函数，用于考生调试使用，请不要修改该程序
def socketServer(callback_fun):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('127.0.0.1', 5555)
    print >> sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    try:
        while True:
            print >> sys.stderr, '\nwaiting to receive message'
            data, addr = sock.recvfrom(4096)

            # print >>sys.stderr, 'received %s bytes from %s' % (len(data), addr)
            print >> sys.stderr, "received cmd: %s" % (data)

            if data:
                ret = callback_fun(data)
                print >> sys.stderr, ret
                length = sock.sendto(ret.encode('utf-8'), addr)
                # print >>sys.stderr, 'sent %s bytes back to %s' % (length, addr)

    finally:
        sock.close()


# 格式化错误码
def format_output(error_code):
    return unicode(error_code)


def transfer_query_result(result_list):
    if not isinstance(result_list, list):
        return unicode(result_list)
    if result_list is None or len(result_list) == 0:
        return constants.S003

    output = ""
    firstone = True
    for result in result_list:
        if firstone:
            firstone = False
            output = result
        else:
            output += "\n" + result

    return output

order_sys = None


# 程序入口，携带入参input_cmd，该参数为字符串类型
def cmd_console(input_cmd):
    args = input_cmd.split()
    cmd = args[0]

    if cmd == "r":
        if len(args) != 1:
            return constants.E001
        return format_output(order_sys.resetSystem())

    elif cmd == "ci":
        if len(args) != 7:
            return constants.E001
        try:
            user_id = int(args[1])
            room_type = str(args[2])
            current_time = int(args[3])
            begin_time = int(args[4])
            end_time = int(args[5])
            count = int(args[6])
            return format_output(order_sys.inputOrderInfo(user_id,
                                                            room_type,
                                                            current_time,
                                                            begin_time,
                                                            end_time,
                                                            count))
        except:
            return constants.E001
    elif cmd == "co":
        if len(args) != 3:
            return constants.E001
        try:
            user_id = int(args[1])
            current_time = int(args[2])
            return format_output(order_sys.inputCheckOutInfo(user_id,
                                                                current_time))
        except Exception as e:
            print(e)
            return constants.E001
    elif cmd == "q":
        try:
            if len(args) == 4:
                query_time = int(args[1])
                room_type = str(args[2])
                status = str(args[3])
            elif len(args) == 3:
                query_time = int(args[1])
                room_type = str(args[2])
                status = None
            else:
                return constants.E001
            return format_output(transfer_query_result(order_sys.queryRoomInfo(query_time, room_type, status)))
        except Exception as e:
            print e.message
            return constants.E001
    elif cmd == "s":
        if len(args) != 2:
            return constants.E001
        try:
            query_sales_time = int(args[1])

            return format_output(constants.S004 % (
                order_sys.querySales(query_sales_time)))
        except:
            return constants.E001

    else:
        return constants.E001


if __name__ == "__main__":
    order_sys = OrderHotelSystem()
    socketServer(cmd_console)
