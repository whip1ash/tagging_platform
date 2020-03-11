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

from django.http import JsonResponse

GET_ERROR_CODE = 998
GET_ERROR_MSG = "This api only support post method!"
POST_ERROR_CODE = 999
POST_ERROR_MSG = "This api only support get method!"

get_method_error = lambda : JsonResponse(fail_resp(code=GET_ERROR_MSG,msg=GET_ERROR_MSG))
post_method_error = lambda : JsonResponse(fail_resp(code=POST_ERROR_CODE,msg=POST_ERROR_MSG))


def success_resp(msg='',data=''):
    return {'success':True,'msg':msg,'code':0,'data':data}

def fail_resp(code,msg,data=''):
    return {'success':False,'msg':msg,'code':code,'data':data}
