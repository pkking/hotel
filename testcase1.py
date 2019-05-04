#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from testaw import *

S000 = "S000:初始化成功"             
S001 = "S001:预订成功"               
S002 = "S002:退房成功"                   
S003 = "S003:没有任何记录"
S004 = "当前营业额为:%s"                       
     
E000 = "E000:非法命令"    
E001 = "E001:参数错误"                 
E002 = "E002:房间数量不够"                   
E003 = "E003:没有该用户的订房信息"                 
E004 = "E004:退房时间超出用户预订时间范围" 
E005 = "E005:该用户所有房间已退" 

class MyTestCase1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return
        
    @classmethod
    def tearDownClass(cls):
        #logging.info('\ntearDownClass：这个类所有用例执行后执行此方法')
        return

    def setUp(self):
        ret = send_cmd("r")
        case_id = self.id()
        logging.info('\n{0} ({1} ...)'.format(case_id.split('.')[-1], case_id))
        #logging.info('setUp：这个类的每个测试用例执行前执行此方法')

    def tearDown(self):
        #logging.info('tearDown：这个类的每个测试用例执行后执行此方法')
        return

    def assertTrue(self, expr, msg=None):
        logging.info('fail %s' % msg if not expr else 'ok')
        super(MyTestCase1, self).assertTrue(expr, msg)

    # 从下面开始编写测试用例
    # 1. 注意具体的测试用例一定要以test开头，用例名禁止使用中文
    # 2. 如果存在多行输出，可以使用\r\n分隔
    def test_TC_00440707_001(self):
        ret = send_cmd("r")
        self.assertEqual(ret, S000)

        ret = send_cmd("ci 1 A 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 1 A 1 1 30 10")
        self.assertEqual(ret, E002)
        
        ret = send_cmd("r")
        self.assertEqual(ret, S000)

    def test_TC_00440707_002(self):
        ret = send_cmd("ci 0 A 1 1 30 10")
        self.assertEqual(ret, E001)

        ret = send_cmd("ci 101 A 1 1 30 10")
        self.assertEqual(ret, E001)

        ret = send_cmd("ci 1 A 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 1 A 1 1 30 10")
        self.assertEqual(ret, E002)

    def test_TC_00440707_003(self):
        ret = send_cmd("ci 1 A 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 2 B 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 3 C 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 2 B 1 1 30 10")
        self.assertEqual(ret, E002)

        ret = send_cmd("ci 3 D 1 1 30 10")
        self.assertEqual(ret, E001)

        std_out = """101 A used 1\r
102 A used 1\r
103 A used 1\r
104 A used 1\r
105 A used 1\r
106 A used 1\r
107 A used 1\r
108 A used 1\r
109 A used 1\r
110 A used 1"""
        ret = send_cmd("q 1 A")
        self.assertEqual(ret, std_out)

        std_out = """201 B used 2\r
202 B used 2\r
203 B used 2\r
204 B used 2\r
205 B used 2\r
206 B used 2\r
207 B used 2\r
208 B used 2\r
209 B used 2\r
210 B used 2"""
        ret = send_cmd("q 1 B")
        self.assertEqual(ret, std_out)

        std_out = """301 C used 3\r
302 C used 3\r
303 C used 3\r
304 C used 3\r
305 C used 3\r
306 C used 3\r
307 C used 3\r
308 C used 3\r
309 C used 3\r
310 C used 3"""
        ret = send_cmd("q 1 C")
        self.assertEqual(ret, std_out)

        ret = send_cmd("s 1")
        self.assertEqual(ret, S004 % (0))

        ret = send_cmd("s 2")
        self.assertEqual(ret, S004 % (6300))

        ret = send_cmd("s 3")
        self.assertEqual(ret, S004 % (12600))

        ret = send_cmd("s 30")
        self.assertEqual(ret, S004 % (182700))

        ret = send_cmd("r")
        self.assertEqual(ret, S000)

        ret = send_cmd("s 30")
        self.assertEqual(ret, S004 % (0))
		
        std_out = """101 A free --\r
102 A free --\r
103 A free --\r
104 A free --\r
105 A free --\r
106 A free --\r
107 A free --\r
108 A free --\r
109 A free --\r
110 A free --"""
		
        ret = send_cmd("q 30 A")
        self.assertEqual(ret, std_out)
		
        std_out = """201 B free --\r
202 B free --\r
203 B free --\r
204 B free --\r
205 B free --\r
206 B free --\r
207 B free --\r
208 B free --\r
209 B free --\r
210 B free --"""
		
        ret = send_cmd("q 30 B")
        self.assertEqual(ret, std_out)
		
        std_out = """301 C free --\r
302 C free --\r
303 C free --\r
304 C free --\r
305 C free --\r
306 C free --\r
307 C free --\r
308 C free --\r
309 C free --\r
310 C free --"""
		
        ret = send_cmd("q 30 C")
        self.assertEqual(ret, std_out)
		
    def test_TC_00440707_004(self):
        ret = send_cmd("ci 2 B 1 4 6 10")
        self.assertEqual(ret, S001)
        
        ret = send_cmd("ci 2 B 1 8 10 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("s 8")
        self.assertEqual(ret, S004 % (3600))

        ret = send_cmd("s 10")
        self.assertEqual(ret, S004 % (7200))

        ret = send_cmd("co 2 8")
        self.assertEqual(ret, E004)
        
        ret = send_cmd("co 2 10")
        self.assertEqual(ret, S002)

    def  test_TC_00440707_005(self):
        ret = send_cmd("ci 1 A 1 1 15 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 1 A 1 15 20 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 2 A 1 20 30 10")
        self.assertEqual(ret, S001)

        
        std_out = """101 A used 1,2\r
102 A used 1,2\r
103 A used 1,2\r
104 A used 1,2\r
105 A used 1,2\r
106 A used 1,2\r
107 A used 1,2\r
108 A used 1,2\r
109 A used 1,2\r
110 A used 1,2"""
        ret = send_cmd("q 20 A")
        self.assertEqual(ret, std_out)

        ret = send_cmd("co 2 1")
        self.assertEqual(ret, S002)

        std_out = """101 A used 1\r
102 A used 1\r
103 A used 1\r
104 A used 1\r
105 A used 1\r
106 A used 1\r
107 A used 1\r
108 A used 1\r
109 A used 1\r
110 A used 1"""
        ret = send_cmd("q 20 A")
        self.assertEqual(ret, std_out)

    def  test_TC_00440707_006(self):
        
        ret = send_cmd("ci 1 A 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 2 B 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("ci 3 C 1 1 30 10")
        self.assertEqual(ret, S001)

        ret = send_cmd("s 30")
        self.assertEqual(ret, S004 % (182700))

        std_out = """101 A used 1\r
102 A used 1\r
103 A used 1\r
104 A used 1\r
105 A used 1\r
106 A used 1\r
107 A used 1\r
108 A used 1\r
109 A used 1\r
110 A used 1"""
        ret = send_cmd("q 1 A")
        self.assertEqual(ret, std_out)

        std_out = """201 B used 2\r
202 B used 2\r
203 B used 2\r
204 B used 2\r
205 B used 2\r
206 B used 2\r
207 B used 2\r
208 B used 2\r
209 B used 2\r
210 B used 2"""
        ret = send_cmd("q 1 B")
        self.assertEqual(ret, std_out)

        std_out = """301 C used 3\r
302 C used 3\r
303 C used 3\r
304 C used 3\r
305 C used 3\r
306 C used 3\r
307 C used 3\r
308 C used 3\r
309 C used 3\r
310 C used 3"""
        ret = send_cmd("q 1 C")
        self.assertEqual(ret, std_out)

        std_out = """101 A used 1\r
102 A used 1\r
103 A used 1\r
104 A used 1\r
105 A used 1\r
106 A used 1\r
107 A used 1\r
108 A used 1\r
109 A used 1\r
110 A used 1"""
        ret = send_cmd("q 30 A")
        self.assertEqual(ret, std_out)

        std_out = """201 B used 2\r
202 B used 2\r
203 B used 2\r
204 B used 2\r
205 B used 2\r
206 B used 2\r
207 B used 2\r
208 B used 2\r
209 B used 2\r
210 B used 2"""
        ret = send_cmd("q 30 B")
        self.assertEqual(ret, std_out)

        std_out = """301 C used 3\r
302 C used 3\r
303 C used 3\r
304 C used 3\r
305 C used 3\r
306 C used 3\r
307 C used 3\r
308 C used 3\r
309 C used 3\r
310 C used 3"""
        ret = send_cmd("q 30 C")
        self.assertEqual(ret, std_out)

    def test_TC_00440707_007(self):
        ret = send_cmd("co 1 1")
        self.assertEqual(ret, E003)

        ret = send_cmd("ci 1 A 9 10 20 1")
        self.assertEqual(ret, S001)

        ret = send_cmd("co 1 1")
        self.assertEqual(ret, E001)

        ret = send_cmd("co 1 10")
        self.assertEqual(ret, E004)

        ret = send_cmd("co 1 12")
        self.assertEqual(ret, S002)

        ret = send_cmd("co 1 12")
        self.assertEqual(ret, E005)

    def test_TC_00440707_008(self):
        ret = send_cmd("ci 1 B 1 4 6 1")
        self.assertEqual(ret, S001)
        
        ret = send_cmd("ci 1 B 1 8 10 1")
        self.assertEqual(ret, S001)

        ret = send_cmd("co 1 3")
        self.assertEqual(ret, S002)

        ret = send_cmd("s 3")
        self.assertEqual(ret, S004 % (0))

        ret = send_cmd("r")
        self.assertEqual(ret, S000)

        ret = send_cmd("ci 1 B 1 4 6 1")
        self.assertEqual(ret, S001)
        
        ret = send_cmd("ci 1 B 1 8 10 1")
        self.assertEqual(ret, S001)

        ret = send_cmd("co 1 7")
        self.assertEqual(ret, S002)

        ret = send_cmd("s 7")
        self.assertEqual(ret, S004 % (360))
            
        ret = send_cmd("r")
        self.assertEqual(ret, S000)
        
        ret = send_cmd("ci 1 B 1 4 6 1")
        self.assertEqual(ret, S001)
        
        ret = send_cmd("ci 1 B 1 8 10 1")
        self.assertEqual(ret, S001)

        ret = send_cmd("co 1 10")
        self.assertEqual(ret, S002)

        ret = send_cmd("s 10")
        self.assertEqual(ret, S004 % (720))


    def test_TC_00440707_009(self):
        ret = send_cmd("ci 1 A 1 1 10 2")
        self.assertEqual(ret, S001)

        std_out = """101 A used 1\r
102 A used 1\r
103 A free --\r
104 A free --\r
105 A free --\r
106 A free --\r
107 A free --\r
108 A free --\r
109 A free --\r
110 A free --"""
        ret = send_cmd("q 5 A")
        self.assertEqual(ret, std_out)

        ret = send_cmd("r")
        self.assertEqual(ret, S000)

        ret = send_cmd("ci 1 A 2 5 10 2")
        self.assertEqual(ret, S001)

        ret = send_cmd("q 1 A")
        self.assertEqual(ret, E001)

        ret = send_cmd("q 3 B used")
        self.assertEqual(ret, S003)

        std_out = """101 A used 1\r
102 A used 1\r
103 A free --\r
104 A free --\r
105 A free --\r
106 A free --\r
107 A free --\r
108 A free --\r
109 A free --\r
110 A free --"""
        ret = send_cmd("q 7 A")
        self.assertEqual(ret, std_out)

        std_out = """101 A used 1\r
102 A used 1"""
        ret = send_cmd("q 7 A used")
        self.assertEqual(ret, std_out)

        std_out = """103 A free --\r
104 A free --\r
105 A free --\r
106 A free --\r
107 A free --\r
108 A free --\r
109 A free --\r
110 A free --"""
        ret = send_cmd("q 7 A free")
        self.assertEqual(ret, std_out)
if __name__ == '__main__':
    stream = open(logfile, 'a')
    # 加载方法1-测试所有用例

    unittest.main(testRunner=unittest.TextTestRunner(stream=stream, verbosity=2))
    # 加载方法2-测试某个类下的所有用例

    # suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase1)
    # unittest.TextTestRunner(stream,verbosity=2).run(suite)

    # 加载方法3-测试单个用例
    # suite = unittest.TestSuite()
    # suite.addTest(MyTestCase1('test_11'))
    # unittest.TextTestRunner(stream,verbosity=2).run(suite)
