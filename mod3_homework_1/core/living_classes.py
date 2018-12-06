#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   classes.py
@Time    :   2018/12/5 16:29
@Desc    :   选课系统的类定义文件  人
'''

from core.utils import CustomError,print_enumerate,file_exist,isnumber
from core.user_auth import write_user_info
from core.dead_classes import *
import pickle
from conf.config import mgr_info
import copy

class Person():
	def __init__(self,name):
		self.name = name

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	def save(self,file):
		f = open(file, 'wb')
		pickle.dump(self, f)
		print('保存成功')

	def exit(self,**kwargs):
		exit('退出程序')

	@classmethod
	def find_person(cls,person_dict,name):
		for p in person_dict:
			if person_dict[p].name == name:
				return person_dict[p]
		else:
			return None

class Teacher(Person):
	operate_lst = [('查看教授课程', 'show_class'),
	               ('查看班级学员', 'show_class_member'),
	               ('退出', 'exit')]

	def __init__(self,name,school):
		Person.__init__(self,name)
		self.school = school
		school.teachers.append(self)
		self.luffy_classes = []


	def show_class(self,title='教授课程',**kwargs):
		print(title)
		print_enumerate(self.luffy_classes)

	def __show_class_member(self,luffy_class,title='班级学员如下'):
		print(title)
		for i,stu in enumerate(luffy_class.students):
			print(i+1,stu,stu.homework_record[str(luffy_class)])
		print('-'*20)

	def show_class_member(self,**kwargs):
		self.show_class(title='选择要查看的课程')
		luffy_class = self.luffy_classes[int(input('>>>').strip())-1]
		self.__show_class_member(luffy_class,'选择要批改作业的学员')
		student = luffy_class.students[int(input('>>>').strip())-1]
		self.__score_a_student(student,luffy_class)

	def __score_a_student(self,student,luffy_class):
		homework = student.homework.get(str(luffy_class))
		if homework:
			homework.show() # 查看作业
		else:
			print('作业还没提交')
			return -1
		progress = student.luffy_classes_progress.get(str(luffy_class))
		score = input('输入评分>>>').strip()
		if isnumber(score):
			score = float(score)
			student.homework_record[str(luffy_class)][progress] = score # 打分
			student.luffy_classes_progress[str(luffy_class)] += 1  # 进度 + 1
			student.homework[str(luffy_class)]=None  #讲作业清空
		return 0


class Student(Person):
	operate_lst = [('查看已选择的课程', 'show_class'),
					('注册', 'register_in'),
				   ('做作业', 'do_homework'),
	               ('退出', 'exit')]

	def __init__(self,name,school):
		Person.__init__(self,name)
		self.school = school
		school.students.append(self)
		self.luffy_class_in = []  # 可能报多个班
		self.luffy_classes_progress = {}
		self.homework={}
		self.homework_record = {}  # 每个班都有一个作业记录，键是 str(class),值是一个record列表


	@property
	def course_names(self): # 从班级列表中提取课程名
		return [x.course.name for x in self.luffy_class_in]

	def show_class(self,title='已选课程',**kwargs):
		print(title)
		for i, luffy_class in enumerate(self.luffy_class_in):
			print(i + 1, luffy_class, '进度', self.luffy_classes_progress[str(luffy_class)])
		print('-' * 20)

	def get_homework(self,luffy_class):
		progress = self.luffy_classes_progress.get(str(luffy_class))
		homework = copy.deepcopy(luffy_class.course.homeworks[progress])
		return homework

	def __do_homework(self,luffy_class):
		home_work = self.get_homework(luffy_class)
		home_work.show()
		home_work.answer = '1+1=2！'
		import time
		time.sleep(2)
		print('上传了答案','1+1=2！')
		self.homework[str(luffy_class)] = home_work

	def do_homework(self,**kwargs):
		self.show_class('选择做哪门课程的作业？')
		luffy_class = self.luffy_class_in[int(input('>>>').strip()) - 1]
		self.__do_homework(luffy_class)


	def __register_in(self, luffy_class):
		course_name = luffy_class.course.name
		if course_name in self.course_names or str(luffy_class) in self.homework_record:
			print('不能重复选课...')
		elif self.name in luffy_class.name_list:
			print('%s已在%s班级注册...'%(self.name,str(luffy_class)))
		else:
			if self.__pay(luffy_class):
				self.luffy_class_in.append(luffy_class)
				self.homework_record[str(luffy_class)]=[-1]*luffy_class.course.num_lessons
				self.luffy_classes_progress[str(luffy_class)] = 0
				self.homework[str(luffy_class)]=None
				luffy_class.students.append(self)
				print('选课成功')
			else:
				pass

	def register_in(self,mgr=None,**kwargs):
		print('有以下课程可选：')
		names = print_enumerate(mgr.luffy_classes)
		luffy_class = mgr.luffy_classes[names[int(input('>>>').strip())-1]]
		self.__register_in(luffy_class)

	def __pay(self, luffy_class):
		amount = luffy_class.course.price
		y = input('Y 确认支付%s 元，其他取消'%amount)
		if y.upper() == 'Y':
			print('成功支付',amount)
			return True
		else:
			print('支付取消')
			return False


class Manager(Person):
	operate_lst = [('查看校区', 'show_school'),
	               ('创建课程', 'create_course'),
	               ('查看课程', 'show_course'),
	               ('创建讲师', 'create_teacher'),
	               ('查看讲师', 'show_teacher'),
	               ('创建班级', 'create_class'),
	               ('查看班级', 'show_class'),
	               ('创建学员', 'create_student'),
	               ('查看学员', 'show_student'),
	               ('退出', 'exit')]

	def __init__(self,name):
		Person.__init__(self, name)
		self.schools = {}
		self.courses = {}
		self.luffy_classes = {}
		self.teachers = {}
		self.students = {}

	@classmethod
	def from_data(self,file):
		if file_exist(file):
			return pickle.load(open(file,'rb'))
		else:
			return Manager('Cortana')

	def __create_school(self,**kwargs):  # 禁用此方法
		self.schools['Beijing Shahe']=School('Beijing Shahe')
		self.schools['Shanghai Minhang']=School('Shanghai Minhang')

	def show_school(self,verb=True,**kwargs):
		if verb:
			print_enumerate(self.schools)
		return self.schools

	def create_course(self,**kwargs):
		print('选择开课校区')
		indexes = print_enumerate(self.schools)
		sch = self.schools[indexes[int(input('>>>').strip()) - 1]]
		course_name = input('输入课程名：')
		period = input('输入课程周期：').strip()
		price = float(input('输入课程价格：').strip())
		self.courses[course_name] = (
			Course(course_name, period, price, sch, [Homework('print(\'helloworld\')')] * 30))

	def show_course(self,verb=True,**kwargs):
		if verb:
			print_enumerate(self.courses)
		return self.courses

	def create_class(self,**kwargs):
		print('选择课程')
		indexes = print_enumerate(self.courses)
		course = self.courses[indexes[int(input('>>>').strip()) - 1]]
		print('选择讲师')
		indexes = print_enumerate(self.teachers)
		teacher = self.teacher[indexes[int(input('>>>').strip()) - 1]]
		class_name_suffix = input('输入班级后缀名：')
		self.luffy_classes[str(course)+' '+class_name_suffix] = Luffy_class(class_name_suffix, course, teacher)

	def show_class(self,verb=True,**kwargs):
		if verb:
			print_enumerate(self.luffy_classes)
		return self.luffy_classes

	def create_teacher(self,**kwargs):
		print('选择任教校区')
		indexes = print_enumerate(self.schools)
		sch = self.schools[indexes[int(input('>>>').strip()) - 1]]
		teacher_name = input('输入讲师名：')
		passwd= input('输入密码：')
		self.teachers[teacher_name] = Teacher(teacher_name, sch)
		write_user_info(teacher_name,passwd,'Teacher')

	def show_teacher(self,verb=True,**kwargs):
		if verb:
			print_enumerate(self.teachers)
		return self.teachers

	def create_student(self,**kwargs):
		print('选择校区')
		indexes = print_enumerate(self.schools)
		sch = self.schools[indexes[int(input('>>>').strip()) - 1]]
		stu_name = input('输入学生名：')
		passwd = input('输入密码：')
		self.students[stu_name] = Student(stu_name, sch)
		write_user_info(stu_name, passwd, 'Student')

	def show_student(self,verb=True,**kwargs):
		if verb:
			print_enumerate(self.students)
		return self.students

	def save_self(self):
		self.save(mgr_info)

	# --------------------------------
	def do_it_all_for_testing(self):

		self.schools['Beijing Shahe'] = School('Beijing Shahe')
		self.schools['Shanghai Minhang'] = School('Shanghai Minhang')

		bj = self.schools['Beijing Shahe']
		sh = self.schools['Shanghai Minhang']

		self.courses['Python Full Stack'] = (
			Course('Python Full Stack', '6 month', 43210, bj, [Homework('print(\'helloworld\')')] * 30))
		self.courses['Linux Operation'] = (
			Course('Linux Operation', '5 month', 54321, bj, [Homework('rm -rf /*')] * 25))
		self.courses['Goto Hell'] = (
			Course('Goto Hell', '8 month', 65432, sh, [Homework('fmt.Println("gotohell")')] * 35))


		py = self.courses['Python Full Stack']
		linux = self.courses['Linux Operation']
		go = self.courses['Goto Hell']

		self.teachers['alex'] = Teacher('alex', bj)
		self.teachers['sally'] = Teacher('sally', sh)
		self.teachers['zuckberg'] = Teacher('zuckberg', bj)

		alex = self.teachers['alex']
		sally = self.teachers['sally']
		zuck = self.teachers['zuckberg']

		self.luffy_classes['Python Full Stack S6'] = Luffy_class('S6', py, alex)
		self.luffy_classes['Goto Hell S3'] = Luffy_class('S3', go, sally)
		self.luffy_classes['Linux Operation S22'] = Luffy_class('S3', linux, zuck)

		self.students['zhanghu'] = Student('zhanghu', bj)
		self.students['xiaopang'] = Student('xiaopang', sh)
		self.students['nana'] = Student('nana', bj)
		self.students['duangduangge'] = Student('duangduangge', bj)
		self.students['brickhead'] = Student('brickhead', bj)

		self.students['xiaopang']._Student__register_in(alex.luffy_classes[0])
		self.students['zhanghu']._Student__register_in(alex.luffy_classes[0])
		self.students['nana']._Student__register_in(alex.luffy_classes[0])
		self.students['duangduangge']._Student__register_in(zuck.luffy_classes[0])
		self.students['brickhead']._Student__register_in(sally.luffy_classes[0])

		self.save(mgr_info)


if __name__ == '__main__':
	mgr = Manager('Cortana')
	mgr.do_it_all_for_testing()

	# wang.do_homework(alex.luffy_classes[0])
	# alex.score_a_student(wang,alex.luffy_classes[0])
	# alex.show_class_member(alex.luffy_classes[0])
	#
	# wang.do_homework(alex.luffy_classes[0])
	# alex.score_a_student(wang, alex.luffy_classes[0])
	#
	# alex.show_class_member(alex.luffy_classes[0])


