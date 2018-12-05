#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/12/5 17:55
@Desc    :
'''
class CustomError(BaseException):
	def __init__(self,msg):
		BaseException.__init__(self)
		self.msg = msg

	def __str__(self):
		return self.msg


if __name__ == '__main__':
	raise CustomError('sadasdsadas')
