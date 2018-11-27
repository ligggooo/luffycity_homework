#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/11/27 9:10
@Desc    :
'''
import json

from core.auth import auth_passwd,login

@auth_passwd
def transfer():
	pass

@login
def withdraw():
	pass

@login
def repay():
	pass


@login
def check_account():
	return 0


@auth_passwd
def atm_pay(amount):
	if amount > 1099:
		return False
	else:
		return True

if __name__ == '__main__':
	pass
