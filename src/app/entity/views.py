# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import EntityType,EntityTag

import json

def list_entity_type(request):
    '''
    获取实体类型列表
    :param request:
    :return:
    {"success": true, "msg": "", "code": 0, "data": [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}, {"id": 3, "name": "c"}, {"id": 4, "name": "d"}, {"id": 5, "name": "e"}]}
    '''

    response_data = list(EntityType.objects.all().values())
    return JsonResponse(success_resp(data=response_data))

def add_entity_type(request):
    '''
    增加实体类型
    :param request: input data format
    {'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''

    body = json.loads(request.body)
    entity_type = body.get('type')

    try:
        records = EntityType(name=entity_type)
        records.save()
    except:
        return JsonResponse(fail_resp(code=1,msg='Add entity type failed!'))

    return JsonResponse(success_resp(msg="Add entity type success!"))


def del_entity_type(request):
    '''

    :param request:
    {'id':int,'type':'f'}
    :return:
    '''
    pass

def edit_entity_type(request):
    '''

    :param request:
    {'id':int,'type':'f'}
    :return:
    '''
    pass