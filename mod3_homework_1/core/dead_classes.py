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
		self.teachers=[]
		self.students=[]

	def new_course(self,name,period,price,school,homeworks):
		course_new = Course(name,period,price,school,homeworks) # 创建课程关联学校
		return course_new

	def new_class(self,class_name,course,teacher):
		class_new = Luffy_class(class_name,course,teacher)  # 创建班级关联学校
		return class_new

	def __str__(self):
		return self.addr

class Homework:
	def __init__(self,detail):
		self.detail = detail
		self.answer = ''
		self.score = 0

	def show(self):
		print('题目：', self.detail)
		print('答案：', self.answer)

class Course:
	def __init__(self,name,period,price,school,homeworks):
		self.name = name
		self.period = period
		self.price = price

		self.school = school   # A School object  关联学校
		school.courses.append(self)

		self.classes = []
		self.homeworks = homeworks    # A list of Homework objects

	@property
	def	num_lessons(self):
		return len(self.homeworks)

	def __str__(self):
		return self.name+','+self.school.addr

	def __repr__(self):
		return self.__str__()

class Luffy_class:
	def __init__(self,class_name,course,teacher):
		self.course = course  # 关联课程
		course.classes.append(self)
		course.school.classes.append(self) # 关联学校

		self.class_name = class_name
		self.students = []
		self.teacher = teacher  #关联讲师
		teacher.luffy_classes.append(self)

		self.progress = {0,course.num_lessons}  # eg. python S6 (0,30) at

	@property
	def name_list(self):
		return [stu.name for stu in self.students]

	def __str__(self):
		return self.course.name +','+self.class_name

	def __repr__(self):
		return self.__str__()




