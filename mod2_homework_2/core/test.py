#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   test.py
@Time    :   2018/11/26 9:07
@Desc    :
'''
import os

def fun():
	print(os.path.abspath(__file__))
	print(os.path.abspath('.'))

if __name__ == '__main__':
	pass
