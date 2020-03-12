# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import RelationTag,RelationType
from app.normal.models import Sentence

import json
from django.forms.models import model_to_dict

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


# 以下是api接口
def save(request):
    '''
    save tag
    {"tag_id":int,"sentence_id":int,"head_pos":"x(int),y(int)","head_entity":"jlkjlkkkkk","tail_entity":"asdfasdfasdfasdf",tail_entity_pos,"type":int}
    :param request:
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    tag_id = int(body.get('tag_id')) if int(body.get('tag_id')) > 0 else 0
    sentence_id = int(body.get('sentence_id'))

    head_entity = body.get('head_entity')
    head_pos = body.get('head_pos')
    if not verify_pos(head_pos):
        return JsonResponse(fail_resp(code=WRONG_PARAM_CODE,msg="Wrong parameter[head_pos]"))
    tail_entity = body.get('tail_entity')
    tail_pos = body.get('tail_pos')
    if not verify_pos(tail_pos):
        return JsonResponse(fail_resp(code=WRONG_PARAM_CODE,msg="Wrong parameter[tail_pos]"))
    type = int(body.get('type'))

    # update
    if tag_id != 0:
        try:
            tag = RelationTag.objects.get(id=tag_id)
        except Exception as e:
            return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE,msg="Wrong tag_id",data=get_exception(e)))

        tag.sentence_id = sentence_id
        tag.head_entity = head_entity
        tag.head_entity_pos = head_pos
        tag.tail_entity = tail_entity
        tag.tail_entity_pos = tail_pos
        tag.type = type

        try:
            tag.save()
        except Exception as e:
            return JsonResponse(fail_resp(code=SAVE_FAILED_CODE,msg=SAVE_FAILED_MSG,data=get_exception(e)))
    #create
    else:
        tag = RelationTag(sentence_id=sentence_id,head_entity=head_entity,head_pos=head_pos,tail_entity=tail_entity,tail_pos=tail_pos,type=type)

        try:
            tag.save()
        except Exception as e:
            return JsonResponse(fail_resp(code=SAVE_FAILED_CODE,msg=SAVE_FAILED_MSG,data=get_exception(e)))

    return JsonResponse(success_resp(msg=SAVE_SUCCESS_MSG))
        


def list_all(request):
    '''
    查看历史打标数据,分页
    :param request:
    :return: int 数量
    '''

    if request.method == "POST":
        return post_method_error()

    body= json.loads(request.body)
    page = int(body.get('page')) if int(body.get('page')) > 0 else 0
    limit = int(body.get('limit'))
    offset = page2offset(page,limit)

    try:
        tags = list(RelationTag.objects.all()[offset:limit].values())
    except Exception as e :
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="List all relation tags failed !",data=get_exception(e)))

    return JsonResponse(success_resp(data=tags))

def count(request):
    '''
    数据数量，考虑是否要合并到list接口中
    :param request:
    :return:
    '''
    if request.method == "POST":
        return post_method_error()

    try:
        num = RelationTag.objects.count()
    except Exception as e :
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Get relation tag count failed!",data=get_exception(e)))

    return JsonResponse(success_resp(data={"count":num}))

def delete(request):
    '''
    delete a tag
    :param request: {'id':int}
    :return: {'success':True,'msg':'Delete tag success!','code':0,'data':data}
    '''

    if request.method == "GET":
        return get_method_error()


    body = json.loads(request.body)
    tag_id = int(body.get('id'))

    if not exist_sentence(tag_id):
        return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE,msg="This tag does't haverelate sentence"))

    try:
        RelationTag.objects.get(pk=tag_id).delete()
    except:
        return JsonResponse(fail_resp(code=DELETE_ERROR,msg='Delete tag failed!'))

    return JsonResponse(success_resp(msg="Delete tag success!"))



def edit(request):
    '''
    此接口保留不实现，edit功能同save
    :param request:
    :return:
    '''

    pass


def get(request):
    '''
    拿一条特定的数据。
    :param request: {'id':int}
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    tag_id = int(body.get('id'))

    try:
        tag_data = model_to_dict(RelationTag.objects.get(id=tag_id))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Failed to get a relation tag record"),data=get_exception(e))
    return JsonResponse(success_resp(msg="Get tag success!",data=tag_data))


def list_relation_type(request):
    response_data = list(RelationType.objects.all().values())
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
        return get_method_error()

    body = json.loads(request.body)
    relation_type = body.get('type')

    try:
        records = RelationType(name=relation_type)
        records.save()
    except:
        return JsonResponse(fail_resp(code=SAVE_FAILED_CODE,msg='Add relation type failed!'))

    return JsonResponse(success_resp(msg=SAVE_SUCCESS_MSG))


def del_relation_type(request):
    '''
    删除关系类型
    :param request:
    {'id':int,'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    relation_id = int(body.get('id'))

    try:
        records = list(RelationTag.objects.filter(type__id=relation_id).all().values())
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Get tags by type failed!"),data=get_exception(e))


    if not records:
        return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE,msg="A wrong tag id"))

    for item in records:
        if not exist_sentence(item['id']):
            return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE,msg="This tag does't have relate sentence"))

    try:
        RelationType.objects.get(pk=relation_id).delete()
    except:
        return JsonResponse(fail_resp(code=DELETE_ERROR,msg='Delete relation type failed!'))

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
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    relation_id = int(body.get('id'))
    relation_type = body.get('type')

    try:
        records = RelationType.objects.get(pk=relation_id)
        records.name = relation_type
        records.save()
    except:
        return JsonResponse(fail_resp(code=SAVE_FAILED_CODE,msg='Edit relation type failed!'))

    return JsonResponse(success_resp(msg="Edit relation type success!"))

def exist_sentence(relation_id):
    try:
        num = RelationTag.objects.filter(sentence_id__id=relation_id).count()
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR),msg="Get number of relation tags failed!",data=get_exception(e))

    if num == 0 :
        return False
    elif num == 1 :
        try:
            tag = RelationTag.objects.get(id=relation_id)

            sentence = Sentence(id=tag.sentence_id_id)
            sentence.relation_tag = False
            sentence.save()
        except Exception as e:
            return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Change sentence entity tag flag faild"),data=get_exception(e))

        else:
            return True
