#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   classes.py
@Time    :   2018/12/5 16:29
@Desc    :   选课系统的类定义文件  人
'''

from core.utils import CustomError
from core.dead_classes import Luffy_class

class Person():
	def __init__(self,name):
		self.name = name

class Teacher(Person):
	def __init__(self,name,school):
		Person.__init__(self,name)
		self.school = school
		self.classes = []

class Student(Person):
	def __init__(self,name,school):
		Person.__init__(self,name)
		self.school =school
		self.luffy_class_in = []  # 可能报多个班
		self.homework_record = {}  # 每个班都有一个作业记录，键是 str(class),值是一个record列表

	@property
	def course_in(self):
		return [x.course.name for x in self.luffy_class_in]

	def register_in(self,luffy_class):
		course_name = luffy_class.course.name
		if course_name in self.course_in or str(luffy_class) in self.homework_record:
			raise CustomError('不能重复选课...')
		elif self.name in luffy_class.name_list:
			raise CustomError('%s已在%s班级注册...'%(self.name,str(luffy_class)))
		else:
			if self.__pay(luffy_class):
				self.luffy_class_in.append(luffy_class)
				self.homework_record[str(luffy_class)]=[]
				luffy_class.students.append(self)
			else:
				pass

	def __pay(self,luffy_class):
		amount = luffy_class.course.price
		print('Pay',amount)
		return True

class Manager(Person):
	def __init__(self,name):
		Person.__init__(self,name)



