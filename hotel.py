# -*- coding:UTF-8 -*-
from __future__ import print_function
import logging
from constants import *

import sys
TIME_LEN = 30

PRICE = {
    "A": 150,
    "B": 180,
    "C": 300
}

EMPTY = 0
LIVED = 1
CHK_IN = 2
CHK_OUT = 3

logger = logging.getLogger('')
shandler = logging.StreamHandler(sys.stdout)
handler = logging.FileHandler(
    "hotellog")
formatter = logging.Formatter(
    '[%(asctime)s][%(levelname)s][%(message)s][%(filename)s:%(lineno)d,%(funcName)s][pid:%(process)d(%(processName)s),tid:%(thread)d(%(threadName)s)]')
#handler.setFormatter(formatter)
#logger.addHandler(handler)
shandler.setFormatter(formatter)
logger.addHandler(shandler)

print("seraf")

class RoomMgr(object):
    def __init__(self):
        self.sys_time = 0
        self.rooms = {
            "A": [Room(i+100, "A") for i in range(1, 11)],
            "B": [Room(i+200, "B") for i in range(1, 11)],
            "C": [Room(i+300, "C") for i in range(1, 11)]
        }
        self.users = []
        self.orders = []
        global logger


    def check_uid(self, uid):
        if uid >= 1 and uid <= 100:
            return True
        else:
            print("invalid uid {}".format(uid))
            return False

    def get_user(self, uid):
        for u in self.users:
            if uid == u.id:
                return u
        u = User(uid, self)
        self.users.append(u)
        return u

    def get_sales(self, now):
        if not self.check_time(now):
            return E001
        
        sales = 0
        for r in self.rooms["A"]:
            sales += r.get_sales(now)
        for r in self.rooms["B"]:
            sales += r.get_sales(now)
        for r in self.rooms["C"]:
            sales += r.get_sales(now)
        return sales
        
    def order(self, uid, room_type, begin, end, count, now):
        print("uid:{} room_type:{} begin:{} end:{} count:{} now:{}".format(uid, room_type, begin, end, count, now))
        if count > 10:
            print("not enough room for {}".format(count))
            return E001
        if count <= 0:
            print('invalid count:{}'.format(count))
            return E001

        if not self.check_time(now, begin, end):
            return E001
        if not self.check_uid(uid):
            return E001
        rooms = []
        order = Order(self.get_user(uid),  begin, end, count)
        for r in self.rooms[room_type]:
            if count == len(rooms):
                break
            if not r.can_order(order):
                return E002
            rooms.append(r)
        for r in self.rooms[room_type]:
            order.rooms.append(r)
            r.order(order)
        return S001

    def unorder(self, uid, now):
        if not self.check_uid(uid):
            return E001
        u = self.get_user(uid)
        u.CheckOut(now)
        return S002

    def check_time(self, now, begin=0, end=29):
        if begin < 0:
            print('begin time:{} cant less than 0'.format(
                begin))
            return False
        if end > 29:
            print('end time:{} cant bigger than 29'.format(
                begin))
            return False
        if now < self.sys_time:
            print('operate time({}) cannot less than sys_time({})'.format(
                now, self.sys_time))
            return False
        if begin > end:
            print('begin time({}) cannot bigger than end time({})'.format(
                begin, end))
            return False
        if now > end:
            print('oprate time({}) cannot bigger than end time({})'.format(
                now, end))
            return False
        if now < begin:
            print('oprate time({}) cannot less than begin time({})'.format(
                now, begin))
            return False
        return True

    def check_room_type(self, room_type):
        if room_type != u"A" and room_type != u"B" and room_type != u"C":
            return False
        return True

    def get_status(self, now, room_type, status):
        print('get_status now:{} room_type:{} status({})'.format(now, room_type, status))
        if not self.check_room_type(room_type):
            print("invalid room type:{}".format(room_type))
            return E001
        if not self.check_time(now):
            return E001
        if status != "used" and status != "free" and status != None:
            print('invalid status({})'.format(status))
            return E001
        if status == None:
            tmp_status = "used,free"
            print('status({}) convert to {}'.format(status, tmp_status))
        else:
            tmp_status = status
        out = []
        for r in self.rooms[room_type]:
            status_output = r.print_status(now, tmp_status)
            if status_output:
                print('get status:{}'.format(status_output))
                out.append(status_output)
        return out


class Status(object):
    status_table = {
        LIVED: "used",
        CHK_OUT: "used",
        CHK_IN: "used",
        EMPTY: "free"
    }

    def __init__(self, status, uids):
        self.status = status
        self.uids = uids

    def print_status(self):
        user_str = ""
        for u in self.uids:
            user_str += str(u)+','
        return "{} {}".format(self.status_table[self.status], user_str[:-1])

    def add_user(self, user):
        if user.id not in self.uids:
            self.uids.append(user.id)

    def __repr__(self):
        if self.status == CHK_IN:
            return "check_in"
        elif self.status == CHK_OUT:
            return "check_out"
        elif self.status == LIVED:
            return "lived"
        elif self.status == EMPTY:
            return "empty"
        else:
            return "invalid status"

    def rm_user(self, user):
        if user.id in self.uids:
            self.uids.remove(user.id)
        else:
            print('no uid:{} in status'.format(user.id))


class Room(object):
    def __init__(self, id, room_type):
        self.id = id
        self.room_type = room_type
        self.price = PRICE[room_type]
        self.status = [Status(EMPTY, [])]*30
        self.orders = []

    def get_sales(self, now):
        sales = 0
        for o in self.orders:
            sales += o.get_sale_days(now)*self.price
        return sales

    def can_order(self, order):
        if self.status[order.begin].status == LIVED:
            print(
                'cant order because day:{} already lived by:{}'.format(order.begin, self.status[order.begin].uids))
            return False
        if self.status[order.begin].status == CHK_IN:
            print(
                'cant order because day:{} already in check_in status by:{}'.format(order.begin, self.status[order.begin].uids))
            return False
        if self.status[order.end].status == LIVED:
            print(
                'cant order because day:{} already in lived status by:{}'.format(order.end, self.status[order.begin].uids))
            return False
        if self.status[order.end].status == CHK_OUT:
            print(
                'cant order because day:{} already in check out status by:{}'.format(order.end, self.status[order.begin].uids))
            return False

        for t in range(order.begin+1, order.end):
            if self.status[t].status != EMPTY:
                print('cant order because {} already in check {} status by:{}'.format(
                    order.end, str(self.status[t]), self.status[order.begin].uids))
                return False
        return True

    def order(self, order):
        self.orders.append(order)
        self.status[order.begin].status = CHK_IN
        self.status[order.begin].add_user(order.user)
        self.status[order.end].status = CHK_OUT
        self.status[order.end].add_user(order.user)

        for t in range(order.begin+1, order.end):
            self.status[t].status = LIVED
            self.status[t].add_user(order.user)

    def unorder(self, order, now):
        self.orders.remove(order)
        if order.end < now:
            self.sales = self.price * (order.end - order.begin)
        else:
            self.sales = self.price * (now - order.begin)
        order.cancel()
        for t in range(order.begin, order.end+1):
            self.status[t].status = EMPTY
            self.status[t].rm_user(order.user)

    def print_status(self, now, status):
        s = self.status[now]
        #print(s.__dict__)
        if "free" in status and (s.status == LIVED or s.status == CHK_IN or s.status == CHK_OUT):
            return
        if "used" in status and s.status == EMPTY:
            return
        return "{} {} {} {}".format(
            self.id, self.room_type, now, s.print_status())


class User(object):
    def __init__(self, id, RoomMgr):
        self.id = id
        self.orders = []
#        self.RoomMgr = RoomMgr
    '''
    def OrderRoom(self, room_type, begin, end, count, now):
        orders = self.RoomMgr.order(room_type, begin, end, count, now)
        self.orders.extend(orders)
        if orders == []:
            return False
        else:
            return True
    '''

    def CheckOut(self, now):
        for o in self.orders:
            o.cancel(now)


class Order(object):
    def __init__(self, user, begin, end, count):
        self.user = user
        self.begin = begin
        self.end = end
        self.rooms = []

    def cancel(self, now):
        for r in self.rooms:
            r.unorder(self, now)

    def __repr__(self):
        return "order:begin:{} end:{} uid:{}".format(self.begin, self.end, self.user.id)

    def get_sale_days(self, now):
        if self.end > now:
            end = now
        pay_days = end - self.begin
        print('order({}) have to pay:{} days'.format(str(self), pay_days))
        return pay_days


class OrderHotelSystem(object):
    '''
        说明：
        （1）考生需要根据考题要求，实现相应的接口。可以根据需要增加变量或方法。
        （2）constants.py文件中已经预定义了一些常量值，测试用例会引用这些常量。涉及到这些常量，考生应该直接引用。
        （3）接口返回成功或失败代码时，请直接返回预定义的常量。如：return constants.E002
    '''

    '''以下是考生需要实现的接口'''
    def resetSystem(self):
        '''
            功能接口：系统初始化
        '''
        
        self.isInit = True
        self.mgr = RoomMgr()
        return S000

    def inputOrderInfo(self, userId, roomType, currentTime, beginTime, endTime, count):
        '''
            功能接口：录入客户预订信息
        '''
        
        if not self.isInit:
            return E001
        return self.mgr.order(userId, roomType, beginTime-1, endTime-1, count, currentTime-1)

    def inputCheckOutInfo(self, userId, currentTime):
        '''
            功能接口：录入客户退房信息
        '''
        
        if not self.isInit:
            return E001
        return self.mgr.unorder(userId, currentTime-1)


    def queryRoomInfo(self, queryTime, roomType, status=None):
        '''
            功能接口：根据状态查询房间信息
            说明：
                当查询记录不存在的时候返回“S003:没有任何记录”
                如果查询记录存在，按返回列表如：["101 A used 2,3","104 A free --"]
        '''
        if not self.isInit:
            return E001
        return self.mgr.get_status(queryTime-1, roomType, status)
                
                
    def querySales(self, queryTime):
        '''
            功能接口：查询系统某一时刻的营业额
        '''
                
        if not self.isInit:
            return E001
        return self.mgr.get_sales(queryTime-1)
