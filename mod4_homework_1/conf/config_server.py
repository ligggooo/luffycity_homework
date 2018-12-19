#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   config.py.py
@Time    :   2018/12/9 17:39
@Desc    :   服务端配置文件
'''

import os
import sys
from threading import Lock


ADDR = '127.0.0.1'
PORT = 8081

__BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = __BASE_DIR+'/data/user_data'
ACC_DIR = __BASE_DIR+'/data/account_data'

THREADING_POOL_SIZE = 3
REQUEST_Q_SIZE = 2

DB_LOCK = Lock()


