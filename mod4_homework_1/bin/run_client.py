#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   run_client.py
@Time    :   2018/12/10 9:22
@Desc    :
'''
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from conf.config_client import ADDR,PORT
from core.client.FTPClient import MYTCPClient

client=MYTCPClient((ADDR,PORT))
client.run()
