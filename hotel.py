#!/bin/env python
# coding=utf-8
import logging
from constants import *

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

logger = logging.getLogger('hotel')
handler = logging.FileHandler(
    "./hotel_log", mode='a', encoding='utf-8', delay=False)
formatter = logging.Formatter(
    '[%(asctime)s][%(levelname)s][%(message)s][%(filename)s:%(lineno)d,%(funcName)s][pid:%(process)d(%(processName)s),tid:%(thread)d(%(threadName)s)]')
handler.setFormatter(formatter)
logger.addHandler(handler)


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
        if count > 10:
            logger.error("not enough room for {}".format(count))
            return E001
        if count <= 0:
            logger.error('invalid count:{}'.format(count))
            return E001

        if not self.check_time(now, begin, end):
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
        u = self.get_user(uid)
        u.CheckOut(now)
        return S002

    def check_time(self, now, begin=0, end=29):
        if begin < 0:
            logger.error('begin time:{} cant less than 0'.format(
                begin))
            return False
        if end > 29:
            logger.error('end time:{} cant bigger than 29'.format(
                begin))
            return False
        if now < self.sys_time:
            logger.error('operate time({}) cannot less than sys_time({})'.format(
                now, self.sys_time))
            return False
        if begin > end:
            logger.error('begin time({}) cannot bigger than end time({})'.format(
                begin, end))
            return False
        if now > end:
            logger.error('oprate time({}) cannot bigger than end time({})'.format(
                now, end))
            return False
        if now < begin:
            logger.error('oprate time({}) cannot less than begin time({})'.format(
                now, begin))
            return False
        return True

    def check_room_type(self, room_type):
        if room_type != u"A" and room_type != u"B" and room_type != u"C":
            return False
        return True

    def get_status(self, now, room_type):
        if not self.check_room_type(room_type):
            logger.error("invalid room type:{}".format(room_type))
            return E001
        if not self.check_time(now):
            return E001
        out = ""
        for r in self.rooms[room_type]:
            out += r.print_status(now) + "\r\n"
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
            logger.error('no uid:{} in status'.format(user.id))


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
            print o.__dict__
            sales += o.get_sale_days(now)*self.price
        return sales

    def can_order(self, order):
        if self.status[order.begin].status == LIVED:
            logger.error(
                'cant order because day:{} already lived by:{}'.format(order.begin, self.status[order.begin].uids))
            return False
        if self.status[order.begin].status == CHK_IN:
            logger.error(
                'cant order because day:{} already in check_in status by:{}'.format(order.begin, self.status[order.begin].uids))
            return False
        if self.status[order.end].status == LIVED:
            logger.error(
                'cant order because day:{} already in lived status by:{}'.format(order.end, self.status[order.begin].uids))
            return False
        if self.status[order.end].status == CHK_OUT:
            logger.error(
                'cant order because day:{} already in check out status by:{}'.format(order.end, self.status[order.begin].uids))
            return False

        for t in range(order.begin+1, order.end):
            if self.status[t].status != EMPTY:
                logger.error('cant order because {} already in check {} status by:{}'.format(
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

    def print_status(self, now):
        for s in self.status:
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
        logger.info('order({}) have to pay:{} days'.format(str(self), pay_days))
        return pay_days


if __name__ == "__main__":
    r = RoomMgr()
    print r.order(1, "A", 0, 30, 10, 1)
    print r.order(1, "A", 0, 30, 10, 1)
