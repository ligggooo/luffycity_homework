#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   Mypool.py
@Time    :   2018/12/16 22:27
@Desc    :   尝试自己实现一个线程池,模仿实现了concurrent.futures线程池的大部分功能

concurrent.futures模块提供了高度封装的异步调用接口
ThreadPoolExecutor：线程池，提供异步调用
ProcessPoolExecutor: 进程池，提供异步调用
Both implement the same interface, which is defined by the abstract Executor class.
基本方法

1、submit(fn, *args, **kwargs)
异步提交任务

2、map(func, *iterables, timeout=None, chunksize=1)
取代for循环submit的操作

3、shutdown(wait=True)
相当于进程池的pool.close()+pool.join()操作
wait=True，等待池内所有任务执行完毕回收完资源后才继续
wait=False，立即返回，并不会等待池内的任务执行完毕
但不管wait参数为何值，整个程序都会等到所有任务执行完毕
submit和map必须在shutdown之前

4、result(timeout=None)
取得结果

5、add_done_callback(fn)
回调函数
fn会把线程任务对象作为参数
'''
import threading
import queue

class Mythreadingpool:
	def __init__(self,num):
		self.capacity = num
		self.job_q = queue.Queue()
		self.workers = []
		for i in range(num):
			t = threading.Thread(target=self.work, args=(self.job_q,))
			self.workers.append(t)
		for t in self.workers:
			t.start()
		self.kill_sig = threading.Event()
		self.kill_sig.clear()

	def work(self,q):
		while 1:
			job = q.get()
			if job is None:
				break
			res = job.run()
			print('done')
			job.result_to_return = res
			job.result_ready.set()

	def submit(self,func,args):
		job = Job(func,args)
		self.job_q.put(job)
		return job

	def join_all(self):
		for i in range(self.capacity):
			self.job_q.put(None)
		for t in self.workers:
			t.join()


class Job:
	def __init__(self,func,args):
		self.func = func
		self.args = args
		self.result_to_return = None
		self.result_ready = threading.Event()
		self.result_ready.clear()

	def result(self):
		self.result_ready.wait()
		return self.result_to_return

	def run(self):
		return self.func(*self.args)


if __name__ == '__main__':
	def test(x,y):
		import time
		print(x, y)
		time.sleep(1)
		return (x+y)

	mypool = Mythreadingpool(100)
	z = []
	for i in range(100):
		z.append(mypool.submit(test, (i, 2)))
	mypool.join_all()
	for zz in z:
		print(zz.result())