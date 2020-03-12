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

RECORD_NOT_EXIST_CODE = 404

SAVE_FAILED_CODE = 1
SAVE_FAILED_MSG = "Save failed!"
SAVE_SUCCESS_MSG = "Save Successed!"

WRONG_PARAM_CODE = 2
WRONG_PARAM_MSG = "You Input wrong parameters!"

DATABASE_ERROR = 3
DELETE_ERROR = 4

get_method_error = lambda : JsonResponse(fail_resp(code=GET_ERROR_MSG,msg=GET_ERROR_MSG))
post_method_error = lambda : JsonResponse(fail_resp(code=POST_ERROR_CODE,msg=POST_ERROR_MSG))

get_exception = lambda e: {"Exception":str(e)}

def success_resp(msg='',data=''):
    return {'success':True,'msg':msg,'code':0,'data':data}

def fail_resp(code,msg,data=''):
    return {'success':False,'msg':msg,'code':code,'data':data}

def verify_pos(pos):
    split_pos = pos.split(',')

    if not split_pos:
        return False

    for item in split_pos:
        if not isinstance(item,int):
            return False
    return True

def page2offset(page,limit):
    return page*limit