#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   config.py.py
@Time    :   2018/12/9 17:39
@Desc    :   客户端配置文件
'''
import os

ADDR = '127.0.0.1'
PORT = 8081

__BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCAL_DATA_DIR = __BASE_DIR+'/data_client/local_data'


