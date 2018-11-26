#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   atm.py
@Time    :   2018/11/26 9:20
@Desc    :   取款机
'''
from core.auth import login,auth_passwd

@login
def account():
	print('atm操作')

if __name__ == '__main__':
	pass
