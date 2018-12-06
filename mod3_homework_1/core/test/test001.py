#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   test001.py
@Time    :   2018/12/5 17:22
@Desc    :   创建测试
'''
from core.dead_classes import *
from core.living_classes import *

if __name__ == '__main__':
	school_bj = School('Beijing Shahe')
	school_sh = School('Shanghai Minhang')

	course_py = Course('Python Full Stack','6 month',43210,school_bj,[Homework('print(\'helloworld\')')]*30)
	course_linux = Course('Linux Operation', '5 month', 54321, school_bj, [Homework('rm -rf /*')] * 25)
	course_go = Course('Goto Hell', '8 month', 65432, school_sh, [Homework('fmt.Println("gotohell")')] * 35)

	print(course_py)
	print(school_bj.courses)

	alex = Teacher('alex',school_bj)
	s1 = Student('zhanghu',school_bj)
	s2 = Student('wangxiaopang',school_sh)
	s3 = Student('nana',school_bj)

	cla1 = Luffy_class('S6',course_py,alex)
	print(cla1)

	s1.register_in(cla1)
	print(s1.luffy_class_in,s1.homework_record)
	print(cla1.students)
