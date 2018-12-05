#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   classes.py
@Time    :   2018/12/5 16:29
@Desc    :   选课系统的类定义文件  系统
'''

class School:
	def __init__(self,addr):
		self.addr = addr
		self.courses = []
		self.classes = []

	def new_course(self,name,period,price,school,homeworks):
		course_new = Course(name,period,price,school,homeworks)
		self.courses.append(course_new)

	def new_class(self,class_name,course,teacher,students):
		class_new = Luffy_class(class_name,course,teacher,students)
		self.classes.append(class_new)

class Homework:
	def __init__(self,detail):
		self.detail = detail

class Course:
	def __init__(self,name,period,price,school,homeworks):
		self.name = name
		self.period = period
		self.price = price

		self.school = school   # A School object  关联学校
		school.courses.append(self)

		self.classes = []
		self.homeworks = homeworks    # A list of Homework objects
		self.num_lessons = len(self.homeworks)

	def __str__(self):
		return self.name+','+self.school.addr

class Luffy_class:
	def __init__(self,class_name,course,teacher):
		self.course = course  # 关联课程
		course.classes.append(self)

		self.class_name = class_name
		self.students = []
		self.teacher = teacher  #关联讲师
		teacher.classes.append(self)

		self.progress = {0,course.num_lessons}  # eg. python S6 (0,30) at

	@property
	def name_list(self):
		return [stu.name for stu in self.students]

	def __str__(self):
		return self.course.name +','+self.class_name





