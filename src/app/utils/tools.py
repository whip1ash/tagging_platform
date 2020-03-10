#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: tools.py
@time: 2020/3/10 21:02
@desc: Some tools
'''

def success_resp(msg='',data=''):
    return {'success':True,'msg':msg,'code':0,'data':data}

def fail_resp(code,msg,data=''):
    return {'success':False,'msg':msg,'code':code,'data':data}

