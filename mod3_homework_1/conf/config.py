#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   config.py
@Time    :   2018/12/6 11:04
@Desc    :
'''

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = base_dir+'/data'

mgr_info = data_dir+'/mgr_info'
user_info = data_dir+'/user_info'