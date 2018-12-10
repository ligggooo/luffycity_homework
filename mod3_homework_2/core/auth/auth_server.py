#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   auth.py
@Time    :   2018/12/9 16:58
@Desc    :   认证模块  服务器端
'''
from conf.config_server import ACC_DIR
import hashlib
import os
import shutil

class Doorkeeper:
	def __init__(self):
		self.db = load_user_db()

	def isvalid(self,head_dict,nounce):
		'''
		用户密码检查
		:param head_dict: # head_dict {'nounce': '1544431817.6', 'name': 'wang', 'sign': 'b43a613bec20bf7de8b95ea8b477617c'}
		:param nounce:  服务器收包时间戳
		:return:
		'''

		print(head_dict,nounce)

		user_nounce = head_dict['nounce']
		sign = head_dict['sign']
		name = head_dict['name']
		info = self.db.get(name)
		if not info: # 查无此人
			return {'status':False,'msg':'查无此人'}
		if abs(float(user_nounce)-float(nounce)) > 3: # 验证信息过期
			return {'status':False,'msg':'验证信息过期'}
		server_sign = hashlib.md5('**'.join([name, info['passwd'], user_nounce]).encode('utf-8')).hexdigest()
		if server_sign == sign:
			return {'status':True,'msg':'验证通过','user':(name,info['space'],info['used'])}
		else: # 密码错误
			return {'status':False,'msg':'密码错误'}

	def update_vol(self,user): # user是一个Customer对象
		name = user.name
		used = user.used
		self.db[name]['used'] = used # 不是必须
		update_db2(name,used) # 写入磁盘

def update_db2(name,used):
	db_file2 = ACC_DIR + '/user_tbl_2'
	db_file2_n = db_file2+'.n'
	f1 = open(db_file2,'r',encoding='utf-8')
	f2 = open(db_file2_n,'w',encoding='utf-8')
	for i,line in enumerate(f1):
		if i == 0:
			f2.write(line)
		else:
			if line.strip().split('|')[0]==name:
				f2.write('%s|%s\n'%(name,used))
			else:
				f2.write(line)
	f1.close()
	f2.close()
	shutil.move(db_file2_n,db_file2)


def load_user_db():
	db_file = ACC_DIR+'/user_tbl'
	user_db={}
	for i,line in enumerate(open(db_file,'r',encoding='utf-8')):
		if i >= 1:
			name, passwd, space = line.strip().split('|')
			user_db[name] = {'passwd':passwd,'space':int(space)*1024*1024}
	db_file2 = ACC_DIR+'/user_tbl_2'
	for i,line in enumerate(open(db_file2,'r',encoding='utf-8')):
		if i >= 1:
			name,used = line.strip().split('|')
			user_db[name]['used'] = int(used)
	return user_db





Heimdallr = Doorkeeper()
pass

if __name__ == '__main__':
	print(Heimdallr.db)