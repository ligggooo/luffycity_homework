#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   atm.py
@Time    :   2018/11/26 9:20
@Desc    :   取款机
'''
from core.auth import auth

@auth
def account():
	print('进入atm机')

if __name__ == '__main__':
	pass
