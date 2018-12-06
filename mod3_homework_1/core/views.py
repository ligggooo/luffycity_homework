#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   views.py
@Time    :   2018/12/6 15:01
@Desc    :   管理员 讲师 学员 视图都在这里实现
			 因为实现思路不一样，无法像教学代码一样使用反射
'''
from core.dead_classes import *
from core.living_classes import *
import sys

def views(name,id):
	mgr = Manager.from_data(mgr_info)
	teachers = mgr.show_teacher(0)
	students = mgr.show_student(0)
	if id == "Manager":
		obj = mgr
	elif id == "Teacher":
		obj = Person.find_person(teachers, name)
	elif id == 'Student':
		obj = Person.find_person(students, name)
	else:
		exit('数据错误')
	if not obj:
		exit('查无此人')
	while 1:
		for id, item in enumerate(obj.operate_lst, 1):
			print(id, item[0])
		try:
			func_str = obj.operate_lst[int(input('>>>').strip()) - 1][1]
		except:
			continue
		print(func_str)
		if hasattr(obj, func_str):
			getattr(obj, func_str)(mgr=mgr)
			mgr.save_self()  # 执行一次保存一次
			input('按任意键回到主菜单')


if __name__ == '__main__':
	# views('alex','Teacher')
	# views('xiaopang', 'Student')
	views('cortana', 'Manager')