# -*- coding:UTF-8 -*-
"""
说明：考生需要实现接口返回值，规格请参考试题规格。
      使用方法请阅读“python考试工程补充说明”
"""
import constants

fee = {constants.SINGLE:150, constants.DOUBLE:180, constants.SUIT:300}
room_type_trans_table = {"A": constants.SINGLE, "B": constants.DOUBLE, "C": constants.SUIT}
room_type_revese_trans = {constants.SINGLE: "A", constants.DOUBLE:"B",  constants.SUIT:"C"}

class roomMgr(object):
    def __init__(self):
        self.single_room = []
        self.double_room = []
        self.suit_room = []
        self.cur_time = 1
        self.users = []
        self.unorderd_users = []
        for i in range(0,10):
            self.single_room.append(room(constants.SINGLE,100+i+1))
            self.double_room.append(room(constants.DOUBLE,200+i+1))
            self.suit_room.append(room(constants.SUIT,300+i+1))

    def check_uid(self, uid):
        return uid <= 100 and uid >= 1


    def get_sales(self, cur_time):
        if not self.check_time(cur_time):
            return constants.E001

        sales = 0
        for i in range(0,10):
            sales += self.single_room[i].getSale(cur_time)
            sales += self.double_room[i].getSale(cur_time)
            sales += self.suit_room[i].getSale(cur_time)
        return sales

    def updateTime(self, cur_time):
        self.cur_time = cur_time
        
    def unorder(self, uid, cur_time):
        if not self.check_uid(uid):
            return constants.E001
        if not self.check_time(cur_time):
            return constants.E001
        
        if uid in self.unorderd_users:
            print "user already checkout self.unorderd_users:{}".format(self.unorderd_users)
            return constants.E005

        if uid not in self.users:
            print "no user info:self.users:{}".format(self.users)
            return constants.E003

        for r in self.single_room:
            ret = r.unorder_by_uid(uid, cur_time)
            if ret == constants.E004:
                print u"unorder time out of range: room:{} time:{} ".format(r.id, cur_time)
                return ret
        for r in self.double_room:
            ret = r.unorder_by_uid(uid, cur_time)
            if ret == constants.E004:
                print u"unorder time out of range: room:{} time:{} ".format(r.id, cur_time)
                return ret
        for r in self.suit_room:
            ret = r.unorder_by_uid(uid, cur_time)
            if ret == constants.E004:
                print u"unorder time out of range: room:{} time:{} ".format(r.id, cur_time)
                return ret
        
        self.updateTime(cur_time)
        if uid in self.users:
            self.users.remove(uid)
        if uid not in self.unorderd_users:
            self.unorderd_users.append(uid)
        return constants.S002

    def get_status(self, cur_time, room_type, status):
        if not self.check_time(cur_time):
            return constants.E001
        print "cur_time:{} room_type:{} status:{}".format(cur_time, room_type, status)
        if "used" != status and "free" != status and status != None:
            return constants.E001

        room_type = room_type_trans_table[room_type]

        if room_type == constants.SINGLE:
            rooms = self.single_room
        elif room_type == constants.DOUBLE:
            rooms = self.double_room
        elif room_type == constants.SUIT:
            rooms = self.suit_room
        else:
            return constants.E001
        result = []
        used = []
        free = []
        for r in rooms:
            if r.status[cur_time-1].live or r.status[cur_time-1].chk_in or r.status[cur_time-1].chk_out:
                print "{} time:{} "
                tmp = ""
                for u in r.status[cur_time-1].uid:
                    tmp += "{},".format(u)
                mark = "uesd {}".format(tmp[:-1])
                used.append("{} {} {}".format(r.id, room_type_revese_trans[r.t], mark))
            else:
                mark = "free --"
                free.append("{} {} {}".format(r.id, room_type_revese_trans[r.t], mark))

        if len(used) + len(free) == 0:
            return constants.S003
        
        if status=="used" or status==None:
            result.extend(used)

        if status=="free" or status==None:
            result.extend(free)

        return result
        
    def check_time(self, cur_time):
        ret = (self.cur_time <= cur_time) and cur_time <= 30 and cur_time >= 1
        if ret == False:
            print "check time error:input cur_time:{} self.cur_time:{}".format(cur_time, self.cur_time)
        return ret

    def order(self, room_type, uid, begin, end, cur_time, num):
        if not self.check_uid(uid):
            return constants.E001
        print "type:{} uid:{} begin:{} end:{} cur_time:{} count:{}".format(room_type, uid, \
            begin, end, cur_time, num)
        
        try:
            room_type = room_type_trans_table[room_type]
        except:
            print "no this type {}".format(room_type)
            return constants.E001
        
        if not self.check_time(cur_time):
            print "no this type {}".format(room_type)
            return constants.E001
        backup_list = []
        if begin < cur_time or cur_time > end or cur_time > 30 \
            or cur_time < 1 or begin > 30 or end > 30 or begin < 1 or \
            end < 1 or begin >= end:
            print "check time error: cur_time:{} this:cur_time:{}".format(cur_time, self.cur_time)
            return constants.E001

        if room_type == constants.SINGLE:
            rooms = self.single_room
        elif room_type == constants.DOUBLE:
            rooms = self.double_room
        elif room_type == constants.SUIT:
            rooms = self.suit_room
        else:
            print "room type error {}".format(room_type)
            return constants.E001

        for i in range(0,num):
            for r in rooms:
                ret = r.canOrder(uid, begin, end)
                if True != ret:
                    continue
                else:
                    self.updateTime(cur_time)
                    backup_list.append(r)
                    r.order(uid, begin, end)
                    break
            if ret != True:
                print "room order failed"
                self.rollback(backup_list)
                return constants.E002
        
        if ret == True:
            if uid not in  self.users:
                self.users.append(uid)
            if uid  in  self.unorderd_users:
                self.unorderd_users.remove(uid)
            return constants.S001
    def rollback_room(self, b):
        if b.t == constants.SINGLE:
            rooms = self.single_room
        elif b.t == constants.DOUBLE:
            rooms = self.double_room
        elif b.t == constants.SUIT:
            rooms = self.suit_room

        for i,r in enumerate(rooms):
            if r.id == id:
                rooms[i] = b

    def rollback(self, backup):
        for b in backup:
            self.rollback_room(b)


class orderStatus(object):
    def __init__(self, chk_in, chk_out, uid, live):
        self.chk_in = chk_in
        self.chk_out = chk_out
        self.uid = [u for u in uid ]
        self.live = live

class room(object):
    def __init__(self, t, id):
        self.sales = 0
        self.t = t
        self.id = id
        self.status = [orderStatus(False, False, [constants.INVALID_UID], False)]*30
        #self.check_out_status = [0]*30

    def updateSale(self, cur_time):
        sales = self.sales
        for i in range(0, cur_time):
            if self.status[i].live or self.status[i].chk_in:
                sales += fee[self.t]
                
            if self.status[i].chk_out:
                self.sales += sales

    def getSale(self, cur_time):
        sales = self.sales
        for i in range(0, cur_time):
            if self.status[i].live or self.status[i].chk_out:
                print "room:{} time:{} fee:{}".format(self.id, i+1, fee[self.t])
                sales += fee[self.t]
                #self.status[i] = orderStatus(False, False, constants.INVALID_UID, False)
        return sales

    def canOrder(self, uid, begin, end):
        if self.status[begin - 1].chk_in or self.status[begin - 1].live:
            return False
        if self.status[end - 1].chk_out or self.status[end - 1].live:
            return False
        
        for i in range(begin,end-1):
            if self.status[i].live or self.status[i].chk_in or \
                self.status[i].chk_out:
                return False

        return True
    
    def unorder_by_uid(self, uid, cur_time):
        found = False
        for i in range(0,30):
            if uid in self.status[i].uid:
                if self.status[cur_time-1].chk_in and uid in self.status[cur_time].uid and not found:
                    return constants.E004
                if self.status[i].chk_out and cur_time > i+1 and not found:
                    print "chk out time {} < cur_time {}".format(i+1, cur_time)
                    return constants.E004
                if self.status[i].chk_in and i+1 > cur_time and not found:
                    print "chk in time {} > cur_time {}".format(i+1, cur_time)
                    return constants.E004
                    
                if not self.status[i].chk_out and i+1 < cur_time:
                    self.sales += fee[self.t]
                
                if self.status[i].chk_in:
                    if uid in self.status[i+1].uid:
                        self.status[i].chk_in = False

                if self.status[i].chk_out:
                    if uid in self.status[i-1].uid:
                        self.status[i].chk_out = False

                if self.status[i].live:
                    self.status[i].live = False

                self.status[i].uid.remove(uid)
                found = True
        
    def order(self, uid, begin, end):
        tmp_uid = [u for u in self.status[begin-1].uid if u != constants.INVALID_UID ]
        if uid not in tmp_uid:
            tmp_uid.append(uid)
        print "now root:{} day:{} live by :{}".format(self.id, begin, tmp_uid)
        self.status[begin-1] = orderStatus(True, False, tmp_uid, False)
        tmp_uid = [u for u in self.status[end-1].uid if u != constants.INVALID_UID ]
        if uid not in tmp_uid:
            tmp_uid.append(uid)
        print "now root:{} day:{} live by :{}".format(self.id, end, tmp_uid)
        self.status[end-1] = orderStatus(False, True, tmp_uid, False)

        for i in range(begin,end-1):
            self.status[i] = orderStatus(False, False, [uid], True)
        
        return constants.S001

    def get_status(self, day):
        if self.status[day-1].live or \
            self.status[day-1].chk_in or \
            self.status[day-1].chk_out:
                return constants.USED
        else:
            return constants.EMPTY
    
    def get_user(self, day):
        if self.get_status(day) == constants.USED:
            return self.status[day-1].uid
        else:
            return [constants.INVALID_UID]

    def checkout_by_uid(self, uid):
        for i in range(0,30):
            if self.status[i].uid == uid:
                self.status[i] = orderStatus(False, False, [constants.INVALID_UID], False)             
				
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
        self.mgr = roomMgr()
        return constants.S000

    def inputOrderInfo(self, userId, roomType, currentTime, beginTime, endTime, count):
        '''
            功能接口：录入客户预订信息
        '''
        
        if not self.isInit:
            return constants.E001
        return self.mgr.order(roomType, userId, beginTime, endTime, currentTime, count)

    def inputCheckOutInfo(self, userId, currentTime):
        '''
            功能接口：录入客户退房信息
        '''
        
        if not self.isInit:
            return constants.E001
        return self.mgr.unorder(userId, currentTime)


    def queryRoomInfo(self, queryTime, roomType, status=None):
        '''
            功能接口：根据状态查询房间信息
            说明：
                当查询记录不存在的时候返回“S003:没有任何记录”
                如果查询记录存在，按返回列表如：["101 A used 2,3","104 A free --"]
        '''
        if not self.isInit:
            return constants.E001
        return self.mgr.get_status(queryTime, roomType, status)
                
                
    def querySales(self, queryTime):
        '''
            功能接口：查询系统某一时刻的营业额
        '''
                
        if not self.isInit:
            return constants.E001
        return self.mgr.get_sales(queryTime)
