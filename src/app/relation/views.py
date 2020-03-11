# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import RelationTag,RelationType

def index(request):
    '''
    todo: 关系打标index页面，存在以下几个链接，查看未/已打标的句子、查看已打标的关系数据、开始打标
    :param request:
    :return:
    '''

    return render(request, 'relation/index.html')

def tag_view(request):
    '''
    todo: 打标的页面
    api: 增加打标/考虑update情况(保存功能)，考虑将add和update两个接口合并、下一条数据(sentence中实现)
    :param request:
    :return:
    '''
    return render(request, 'relation/tag.html')


def tag_history(request):
    '''
    todo 历史打标数据的页面
    api: list、delete、edit、get
    :param request:
    :return:
    '''
    return render(request, 'relation/history.html')


# todo: 以下是api接口
def save(request):
    '''
    todo: save tag
    :param request:
    :return:
    '''
    pass


def list(request):
    '''
    todo: 查看历史打标数据,分页
    :param request:
    :return:
    '''
    pass


def count(request):
    '''
    todo: 数据数量，考虑是否要合并到list接口中
    :param request:
    :return:
    '''
    pass


def delete(request):
    '''
    todo: delete a tag
    :param request:
    :return:
    '''
    pass


def edit(request):
    '''
    todo: 此接口保留不实现，edit功能同save
    :param request:
    :return:
    '''

    pass


def get(request):
    '''
    todo: 拿一条特定的数据。
    :param request:
    :return:
    '''
    pass


def list_relation_type(request):
    response_data = list(RelationType.object.all().value())
    return JsonResponse(success_resp(data=response_data))

def add_relation_type(request):
    '''
    增加关系类型
    :param request: input data format
    {'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''

    if request.method == "GET":
        return JsonResponse(fail_resp(code=GET_ERROR_CODE,msg=GET_ERROR_MSG))

    body = json.loads(request.body)
    relation_type = body.get('type')

    try:
        records = RelationType(name=relation_type)
        records.save()
    except:
        return JsonResponse(fail_resp(code=1,msg='Add relation type failed!'))

    return JsonResponse(success_resp(msg="Add relation type success!"))


def del_relation_type(request):
    '''
    删除关系类型
    :param request:
    {'id':int,'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''
    body = json.loads(request.body)
    relation_id = body.get('id')

    try:
        RelationType.objects.get(pk=relation_id).delete()
    except:
        return JsonResponse(fail_resp(code=1,msg='Delete relation type failed!'))

    return JsonResponse(success_resp(msg="Delete relation type success!"))

def edit_relation_type(request):
    '''
    改变关系类型
    :param request:
    {'id':int,'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''
    body = json.loads(request.body)
    relation_id = body.get('id')
    relation_type = body.get('type')

    try:
        records = RelationType.objects.get(pk=relation_id)
        records.name = relation_type
        records.save()
    except:
        return JsonResponse(fail_resp(code=1,msg='Edit relation type failed!'))

    return JsonResponse(success_resp(msg="Edit relation type success!"))
