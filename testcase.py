#coding=utf-8 
import unittest
from hotel import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TestHotel(unittest.TestCase):

    def setUp(self):
        self.r = RoomMgr()

    def test_init(self):
        self.assertNotEqual(self.r, None)

    def test_order_not_enough(self):
        self.assertEqual(self.r.order(1, "A", 0, 29, 10, 2), S001)
        self.assertEqual(self.r.order(1, "A", 0, 29, 10, 2), E002)

    def test_room_status(self):
        self.assertEqual(self.r.order(1, "A", 0, 29, 10, 2), S001)

        status = u"""101 A 2 used 1\r
102 A 2 used 1\r
103 A 2 used 1\r
104 A 2 used 1\r
105 A 2 used 1\r
106 A 2 used 1\r
107 A 2 used 1\r
108 A 2 used 1\r
109 A 2 used 1\r
110 A 2 used 1\r
"""
        self.assertEqual(self.r.get_status(2,"A"), status)

    def test_room_sales(self):
        self.assertEqual(self.r.order(1, "A", 0, 29, 10, 2), S001)
        self.assertEqual(self.r.get_sales(1), 0)
        self.assertEqual(self.r.get_sales(2), 1500)
if __name__ == '__main__':
    unittest.main()