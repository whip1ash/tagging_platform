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

import re

from django.http import JsonResponse
from app.normal.models import Sentence

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
DATA_REPETATION = 5

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
        if not isinstance(int(item),int):
            return False
    return True

def page2offset(page,limit):
    return page*limit

def index2pos(index,sentence_id):
    try:
        sentence = Sentence.objects.get(id=sentence_id);
    except Exception as e:
        raise e

    content = sentence.content
    sentence_split = content.split(' ')
    entity = sentence_split[index]
    # 妈的，这里先不考虑多个相同的词打不同标记的情况
    entity = re.findall(r'\w*',entity)[0]

    start = content.find(entity)
    offset = start + len(entity)
    return '{},{}'.format(start,offset)



