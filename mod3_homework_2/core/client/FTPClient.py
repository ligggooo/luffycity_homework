#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   FTPClient.py
@Time    :   2018/12/9 11:59
@Desc    :
'''
import socket
import struct
import json
import os
from core.auth.auth_client import login
import time
import hashlib
from conf.config_client import LOCAL_DATA_DIR


class MYTCPClient:
	address_family = socket.AF_INET
	socket_type = socket.SOCK_STREAM
	allow_reuse_address = False
	max_packet_size = 8192
	coding='utf-8'
	request_queue_size = 5
	opration_list = ['ls','cd','mkdir','rm','get','put','vol']

	def __init__(self, server_address, connect=True):
		self.server_address=server_address
		self.socket = socket.socket(self.address_family,
									self.socket_type)
		if connect:
			try:
				self.client_connect()
			except:
				self.client_close()
				raise

	def client_connect(self):
		self.socket.connect(self.server_address)

	def client_close(self):
		self.socket.close()

	@login
	def run(self):
		while True:
			inp=input(">>: ").strip()
			if not inp:continue
			l=inp.split()
			cmd=l[0]
			if cmd in self.opration_list:
				func=getattr(self,cmd)
				func(l)

	def send_auth(self,user_name,passwd): # 这个方法会被 客户端认证模块调用
		nounce = str(round(time.time(),1))
		head_dict = {'name':user_name,'nounce':nounce}
		sign = hashlib.md5('**'.join([user_name, passwd, nounce]).encode('utf-8')).hexdigest()
		head_dict['sign'] = sign
		self.send_dict(head_dict)
		head_back = self.get_header()
		return head_back

	def send_dict(self,header):
		print('-------->发送', header)
		head_json = json.dumps(header)
		head_json_bytes = bytes(head_json, encoding=self.coding)
		head_struct = struct.pack('i', len(head_json_bytes))
		self.socket.send(head_struct)
		self.socket.send(head_json_bytes)

	def get_header(self):
		head_struct = self.socket.recv(4)
		if not head_struct:
			print('连接错误')
			self.socket.close()
		head_len = struct.unpack('i', head_struct)[0]
		head_json = self.socket.recv(head_len).decode(self.coding)
		head_dic = json.loads(head_json)
		return head_dic


	def put(self,args):
		cmd=args[0]
		filename=args[1]
		if not os.path.isfile(filename):
			print('file:%s does not exist' %filename)
			return
		else:
			filesize=os.path.getsize(filename)

		md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()

		head_dic={'cmd':cmd,'filename':os.path.basename(filename),'filesize':filesize,'md5':md5}
		self.send_dict(head_dic)
		head_back = self.get_header()
		if 'error' in head_back:
			print(head_back['error'],'放弃此次传输')
			return
		send_size=0
		with open(filename,'rb') as f:
			for line in f:
				self.socket.send(line)
				send_size+=len(line)
				print('recvsize:%s filesize:%s --%.2f %%--' % (send_size, filesize, send_size / filesize * 100))
			else:
				print('upload successful')
		res = self.get_header()
		print(res) # 服务器会回复校验信息

	def get(self,args):
		target = args[1]
		header = {'cmd': 'get', 'filename': target}
		self.send_dict(header)  # --- 请求头发送完了，等待服务器响应

		header_back = self.get_header()
		print(header_back)
		if 'error' in header_back:
			print(header_back['error'])
			return
		if len(args) <=2:
			local_file_name = target
		else:
			local_file_name = args[2]
		file_path = os.path.normpath(os.path.join(
			LOCAL_DATA_DIR,local_file_name
		))
		print(file_path)
		filesize = header_back['filesize']
		md5 = header_back['md5']

		recv_size = 0
		data = b''
		print('----->', file_path)
		f = open(file_path, 'wb')
		while recv_size < filesize:
			recv_data = self.socket.recv(self.max_packet_size)
			f.write(recv_data)
			data += recv_data
			recv_size += len(recv_data)
			print('recvsize:%s filesize:%s --%.2f %%--' % (recv_size, filesize, recv_size / filesize * 100))
		f.close()

		if hashlib.md5(data).hexdigest() == md5:
			print('校验完毕，文件无损')
		else:
			print('未通过校验，文件已经损坏')

	def ls(self,args):
		header = {'cmd':'ls'}
		self.send_dict(header)
		res = self.get_header()
		print(res['list_dir'])

	def cd(self,args):
		target = args[1]
		header = {'cmd': 'cd','target':target}
		self.send_dict(header)

	def mkdir(self,args):
		target = args[1]
		header = {'cmd': 'mkdir','target':target}
		self.send_dict(header)

	def rm(self,args):
		target = args[1]
		header = {'cmd': 'rm', 'target': target}
		self.send_dict(header)

	def vol(self,args):
		header = {'cmd': 'vol'}
		self.send_dict(header)
		res = self.get_header()
		space, used, left = res['vol_info']
		print('磁盘限额 %.1f M，已经使用 %.1f M，剩余 %.1f M'%(space/1048576, used/1048576, left/1048576))






if __name__ == '__main__':
	pass

