# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import EntityType,EntityTag

import json

def index(request):
    '''
    todo: 实体打标index页面，存在以下几个链接，查看未/已打标的句子、查看已打标的实体数据、开始打标
    :param request:
    :return:
    '''
    return render(request,'entity/index.html')

def tag_view(request):
    '''
    todo: 打标的页面
    api: 增加打标/考虑update情况(保存功能)，考虑将add和update两个接口合并、下一条数据(sentence中实现)
    :param request:
    :return:
    '''
    return render(request,'entity/tag.html')

def tag_history(request):
    '''
    todo 历史打标数据的页面
    api: list、delete、edit、get
    :param request:
    :return:
    '''
    return render(request,'entity/history.html')

# todo: 以下是api接口
def save(request):
    '''
    save tag datal,
    {"sencence_id":int,"pos":"x(int),y(int)","entity":"position","type":int}
    :param request:
    :return:
   {"success": true, "msg": "Save data success", "code": 0, "data": ""}
    '''
    if request.method == "GET":
        return get_method_error()

    

def list_all(request):
    '''
    todo: 查看历史打标数据,分页
    :param request:
    :return:
    '''
    pass

def count(request):
    '''
    todo: 数据数量，考虑是否要合并到list接口中
    :param request: null
    :return: int 数量
    '''
    tag_data = list(EntityTag.objects.all().values)
    return JsonResponse(success_resp(data=len(tag_data)))

def delete(request):
    '''
    todo: delete a tag
    :param request: {'id':int}
    :return: 
    {'success':True,'msg':'Delete tag success!','code':0,'data':data}
    '''
    body = json.loads(request.body)
    tag_id = body.get('id')

    try:
        EntityTag.objects.get(pk=tag_id).delete()
    except:
        return JsonResponse(fail_resp(code=1,msg='Delete tag failed!'))

    return JsonResponse(success_resp(msg="Delete tag success!"))

def edit(request):
    '''
    todo: 此接口保留不实现，edit功能同save
    :param request:{'id':int,'edit_colume':colume_name,'edit_content':content}
    :return: {'success':True,'msg':'Edit tag success!','code':0,'data':data}
    '''


def get(request):
    '''
    todo: 拿一条特定的数据。
    :param request:{'id':int}
    :return:
    '''
    

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

    if request.method == "GET":
        return JsonResponse(fail_resp(code=GET_ERROR_CODE,msg=GET_ERROR_MSG))

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
    删除实体类型
    :param request:
    {'id':int,'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''
    body = json.loads(request.body)
    entity_id = body.get('id')

    try:
        EntityType.objects.get(pk=entity_id).delete()
    except:
        return JsonResponse(fail_resp(code=1,msg='Delete entity type failed!'))

    return JsonResponse(success_resp(msg="Delete entity type success!"))

def edit_entity_type(request):
    '''
    改变实体类型
    :param request:
    {'id':int,'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''
    body = json.loads(request.body)
    entity_id = body.get('id')
    entity_type = body.get('type')

    try:
        records = EntityType.objects.get(pk=entity_id)
        records.name = entity_type
        records.save()
    except:
        return JsonResponse(fail_resp(code=1,msg='Edit entity type failed!'))

    return JsonResponse(success_resp(msg="Edit entity type success!"))
