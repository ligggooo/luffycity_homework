#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/12/5 17:55
@Desc    :
'''

import os
class CustomError(BaseException):
	def __init__(self,msg):
		BaseException.__init__(self)
		self.msg = msg

	def __str__(self):
		return self.msg


def print_enumerate(input):
	# print('-'*20)
	if type(input) == list:
		for i,v in enumerate(input):
			print(i+1,v)
	elif type(input) == dict:
		output = []
		for i,v in enumerate(sorted(input.items())):
			print(i+1,v[0])
			output.append(v[0])
		print('-' * 20)
		return output
	print('-' * 20)

def file_exist(file):
	return os.path.exists(file)

def isnumber(input):
	try:
		float(input)
		return True
	except:
		return False



if __name__ == '__main__':
	# raise CustomError('sadasdsadas')
	print(file_exist(os.path.abspath(__file__)))