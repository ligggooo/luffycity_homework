#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   FTPServer.py
@Time    :   2018/12/9 10:49
@Desc    :   ftp server codes
'''

import hashlib
import socket
import struct
import json
import threading as thr
import os
import time
from core.auth.auth_server import Heimdallr  # the door-keeper
from conf.config_server import DATA_DIR
import traceback
import shutil


class Waitress(thr.Thread):  # 管理多线程
	def __init__(self,conn, addr, server,customer):
		thr.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.server = server
		self.customer = customer

	def run(self):
		print('建立连接',self.addr)
		self.server.job(self.customer)

		self.customer.vol_update() # 异常情况导致传输中断的话，以这种方式完成数据更新
		print(self.customer.name, '容量信息更新完成')
		del self

class Customer:   # 管理用户
	def __init__(self,conn, addr, user_info):
		name,space,used = user_info
		print('初始化用户',addr,name)
		self.conn = conn
		self.addr = addr
		self.name = name
		self.root = self.get_dir()
		self.dir_route = [self.root]
		self.space = space
		self.used = used

	@classmethod
	def getDirSize(cls,dir):  # 增加了一个rm方法支持删除目录，更新用户文件夹容量变得比较麻烦了
		filePath = dir
		size = 0
		for root, dirs, files in os.walk(filePath):
			for f in files:
				size += os.path.getsize(os.path.join(root, f))
		return size

	def vol_change(self,size):
		self.used += size
		self.__save()

	def vol_update(self):
		self.used = self.getDirSize(self.root)
		self.__save()

	def __save(self):
		Heimdallr.update_vol(self)

	def has_enough_volume(self,v):
		if self.used+v >= self.space:
			return False
		else:
			return True

	def get_dir(self):
		root = os.path.join(DATA_DIR,self.name)
		if not os.path.exists(root):
			os.mkdir(root)
		return root

	def cd(self,target):
		r_target = target
		target = os.path.join(self.dir_route[-1], target)
		if r_target == '..' and len(self.dir_route)>= 2:
			self.dir_route.pop()
		elif r_target == '..' and len(self.dir_route) == 1:
			return
		elif os.path.exists(target):
			self.dir_route.append(target)

	def rm(self,target):
		target = os.path.join(self.dir_route[-1], target)
		if os.path.exists(target):
			if os.path.isfile(target):
				vol_del = os.path.getsize(target)
				os.remove(target)
				self.vol_change(-vol_del)
			elif os.path.isdir(target):
				vol_del = self.getDirSize(target)
				shutil.rmtree(target)
				self.vol_change(-vol_del)
			else:
				pass # do nothing


	def ls(self):
		now = self.dir_route[-1]
		list = os.listdir(self.dir_route[-1])
		out = ''
		for i in list:
			target = os.path.join(now,i)
			if (not i.startswith('$')) and os.path.isfile(target):
				# print('%s\t%sbytes'%(i,os.path.getsize(target)))
				out += '%s\t%sbytes\n'%(i,os.path.getsize(target))
			else:
				# print('%s\t文件夹'%i)
				out += '%s\tdirectory\n'%i
		return out

	def mkdir(self,t):
		now = self.dir_route[-1]
		target = os.path.join(now, t)
		if not os.path.exists(target):
			os.mkdir(target)

class MYTCPServer:
	address_family = socket.AF_INET
	socket_type = socket.SOCK_STREAM
	allow_reuse_address = True
	max_packet_size = 8192
	coding='utf-8'
	request_queue_size = 5
	server_dir='file_upload'
	operation_list = ['put', 'get', 'mkdir', 'cd', 'ls', 'rm','vol']  # 限制用户的指令

	def __init__(self, server_address, bind_and_activate=True):
		"""Constructor.  May be extended, do not override."""
		self.server_address=server_address
		self.socket = socket.socket(self.address_family,
									self.socket_type)
		if bind_and_activate:
			try:
				self.server_bind()
				self.server_activate()
			except:
				self.server_close()
				raise

	def server_bind(self):
		"""Called by constructor to bind the socket.
		"""
		if self.allow_reuse_address:
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.server_address)
		self.server_address = self.socket.getsockname()

	def server_activate(self):
		"""Called by constructor to activate the server.
		"""
		self.socket.listen(self.request_queue_size)

	def server_close(self):
		"""Called to clean-up the server.
		"""
		self.socket.close()

	def get_request(self):
		"""Get the request and client address from the socket.
		"""
		return self.socket.accept()

	def close_request(self, request):
		"""Called to clean up an individual request."""
		request.close()

	def run(self):
		while True:
			conn,addr=self.get_request()
			try:
				new_customer,info = self.auth(conn,addr)# 事先约定，客户端建立连接之后第一个数据包是验证信息，只有通过验证才会分配服务员
			except:
				traceback.print_exc()
				continue
			if new_customer:
				self.send_header(conn, addr, info)
				# waitress 会调用server 的job方法，job方法会响应用户请求，调用server的其他方法
				new_waitress = Waitress(conn, addr, self, customer=new_customer)
				new_waitress.start()
			else:
				self.send_header(conn,addr,info)
				conn.close()

	def auth(self,conn,addr):
		head_dict = self.get_header(conn,addr)
		# time.sleep(2)
		nounce = str(round(time.time(), 1))
		info = Heimdallr.isvalid(head_dict, nounce)
		if info['status']:
			return Customer(conn,addr,info['user']),info
		else:
			return None,info

	def get_header(self,conn,addr):
		print('服务器等待请求中')
		head_struct = conn.recv(4)
		if not head_struct:
			print('连接错误')
			conn.close()
		head_len = struct.unpack('i', head_struct)[0]
		head_json = conn.recv(head_len).decode(self.coding)
		head_dic = json.loads(head_json)
		return head_dic #{'auth': 'qqq', 'sign': '2b0cb99468c7be157b70e8f2a7f2b118', 'nounce': '1544349139.4'}

	def send_header(self,conn,addr,header):
		print('发送',header)
		head_json = json.dumps(header)
		head_json_bytes = bytes(head_json, encoding=self.coding)
		head_struct = struct.pack('i', len(head_json_bytes))
		conn.send(head_struct)
		conn.send(head_json_bytes)

	def job(self,customer):  # 服务器的工作方法,被子线程调用，用来处理用户请求
		conn = customer.conn
		addr = customer.addr
		while True:
			try:
				head_dic = self.get_header(conn,addr)
				print(head_dic)
				# head_dic={'cmd':'put','filename':'a.txt','filesize':123123}
				cmd = head_dic['cmd']
				if hasattr(self, cmd) and cmd in self.operation_list:
					func = getattr(self, cmd)
					func(head_dic,customer)
			except ConnectionResetError:
				traceback.print_exc()
				return -1

	def put(self,args,customer):
		conn = customer.conn
		addr = customer.addr
		file_path=os.path.normpath(os.path.join(
			customer.dir_route[-1],
			args['filename']
		))
		print(file_path)
		filesize=args['filesize']
		md5 = args['md5']

		if customer.has_enough_volume(filesize):
			self.send_header(conn, addr, {'msg': 'ok'})
			recv_size=0
			print('----->',file_path)
			f= open(file_path,'wb')
			data =b''
			while recv_size < filesize:
				recv_data= conn.recv(self.max_packet_size)
				f.write(recv_data)
				data += recv_data
				recv_size+=len(recv_data)
				print('recvsize:%s filesize:%s --%.2f %%--' %(recv_size,filesize,recv_size/filesize*100))
			f.close()
			customer.vol_change(int(filesize))

			if hashlib.md5(data).hexdigest() == md5:
				self.send_header(conn,addr,{'msg':'校验完毕，文件无损'})
			else:
				self.send_header(conn,addr,{'error': '校验失败'})
		else:
			self.send_header(conn, addr, {'error': '空间不够'})

	def get(self,args_dict,customer):
		conn = customer.conn
		addr = customer.addr
		filename_relative = args_dict['filename']
		filename = os.path.join(customer.dir_route[-1], filename_relative)
		if not os.path.isfile(filename):
			print('file:%s does not exist' %filename)
			self.send_header(conn,addr, {'error': 'file does not exist'})
			return
		else:
			filesize=os.path.getsize(filename)
		md5 = hashlib.md5(open(filename,'rb').read()).hexdigest()

		header = {'filename':filename_relative,'filesize':filesize,'md5': md5}
		self.send_header(conn,addr,header)

		send_size = 0
		with open(filename, 'rb') as f:
			for line in f:
				conn.send(line)
				send_size += len(line)
				print(send_size)
			else:
				print('send successful')


	def mkdir(self,args_dict,customer):
		target =args_dict['target']
		customer.mkdir(target)

	def cd(self,args_dict,customer):
		target = args_dict['target']
		customer.cd(target)

	def ls(self,args_dict,customer):
		conn = customer.conn
		addr = customer.addr
		list_dir = customer.ls()

		header = {'cmd': 'ls', 'list_dir': list_dir}
		self.send_header(conn, addr, header)

	def rm(self,args_dict,customer):
		target = args_dict['target']
		customer.rm(target)

	def vol(self,args_dict,customer):
		conn = customer.conn
		addr = customer.addr
		space = customer.space
		used = customer.used
		left = space-used
		header = {'cmd': 'ls', 'vol_info': [space,used,left]}
		self.send_header(conn, addr, header)

if __name__ == '__main__':
	c = Customer('','',('wang',100,2))
	print(c)
	print(c.ls())
	c.cd('12')
	print(c.ls())
	c.mkdir('zz')
	c.cd('zz')
	print(c.ls())
	c.cd('..')
	print(c.ls())
	c.cd('..')
	z= c.ls()
	print(c.ls())
	print(c.getDirSize('F:\luffycity\luffycity_homework\mod3_homework_2\core\\auth'))

