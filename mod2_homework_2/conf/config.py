#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   config.py
@Time    :   2018/11/26 11:11
@Desc    :
'''
import os

_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_data_dir = _base_dir+'/data'
user_file = _data_dir+'/user.dat'
