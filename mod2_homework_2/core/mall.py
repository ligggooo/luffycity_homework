#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   mall.py
@Time    :   2018/11/26 9:20
@Desc    :   商城
'''
from core.auth import login,auth_passwd


def cart():
	print('进入购物车')
	pay()

@auth_passwd
def pay():
	print('支出100元')

if __name__ == '__main__':
	cart()
