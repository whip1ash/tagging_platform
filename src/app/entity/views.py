# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import EntityType,EntityTag
from app.normal.models import Sentence

import json
from django.forms.models import model_to_dict

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

# 以下是api接口
def save(request):
    '''
    save tag datal,
    {"tag_id":int,"sentence_id":int,"pos":"x(int),y(int)","entity":"Person","type":int}
    :param request:
    :return:
   {"success": true, "msg": "Save data success", "code": 0, "data": ""}
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    tag_id = int(body.get('tag_id')) if int(body.get('tag_id')) > 0 else 0
    sentence_id = int(body.get('sentence_id'))
    pos = body.get('pos')

    # wrong pos
    if not verify_pos(pos):
        return JsonResponse(fail_resp(code=WRONG_PARAM_CODE,msg="Wrong parameter[pos]"))
    entity = body.get('entity')
    type = int(body.get('type'))

    # update
    if tag_id != 0:
        try:
            tag = EntityTag.objects.get(id=tag_id)
        except EntityTag.DoesNotExist:
            return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE,msg="Wrong tag_id"))

        tag.sentence_id = sentence_id
        tag.pos = pos
        tag.entity = entity
        tag.type = type

        try:
            tag.save()
        except Exception as e:
            return JsonResponse(fail_resp(code=SAVE_FAILED_CODE,msg=SAVE_FAILED_MSG,data=get_exception(e)))
    # create
    else:
        tag = EntityTag(sentence_id=sentence_id,pos=pos,entity=entity,type=type)

        try:
            tag.save()
        except Exception as e:
            return JsonResponse(fail_resp(code=SAVE_FAILED_CODE,msg=SAVE_FAILED_MSG,data=get_exception(e)))

    return JsonResponse(success_resp(msg=SAVE_SUCCESS_MSG))

def list_all(request):
    '''
    查看历史打标数据,分页
    :param request:
    {"page":0,"limit":10}
    :return:
    '''
    if request.method == "POST":
        return post_method_error()

    body = json.loads(request.body)
    page = int(body.get('page')) if int(body.get('page')) > 0 else 0
    limit = int(body.get('limit'))
    offset = page2offset(page,limit)

    try:
        tags = list(EntityTag.objects.all()[offset:limit].values())
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="List all entity tags failed !",data=get_exception(e)))

    return JsonResponse(success_resp(data=tags))


def count(request):
    '''
    数据数量，考虑是否要合并到list接口中
    :param request: null
    :return: int 数量
    '''
    if request.method == "POST":
        return post_method_error()

    try:
        num = EntityTag.objects.count()
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Get entity tag count failed!",data=get_exception(e)))
    return JsonResponse(success_resp(data={"count":num}))

def delete(request):
    '''
    delete a tag 考虑删除sentence问题
    :param request: {'id':int}
    :return: 
    {'success':True,'msg':'Delete tag success!','code':0,'data':data}
    '''

    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    tag_id = int(body.get('id'))

    # verify if need to modify sentence flag
    # 遍历当前表，使用tag_id，tag和relation不通用
    if not exist_sentence(tag_id):
        return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE,msg="This tag does't have relate sentence"))
    try:
        EntityTag.objects.get(pk=tag_id).delete()
    except:
        return JsonResponse(fail_resp(code=DELETE_ERROR,msg='Delete tag failed!'))

    return JsonResponse(success_resp(msg="Delete tag success!"))

def edit(request):
    '''
    此接口保留不实现，edit功能同save
    :param request:
    :return: 
    '''


def get(request):
    '''
    拿一条特定的数据。
    :param request:{'id':int}
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    tag_id = body.get('id')

    try:
        tag_data = model_to_dict(EntityTag.objects.get(id=tag_id))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Failed to get a entity type record.",data=get_exception(e)))

    return JsonResponse(success_resp(msg="Get tag success!",data=tag_data))

def list_entity_type(request):
    '''
    获取实体类型列表
    :param request:
    :return:
    {"success": true, "msg": "", "code": 0, "data": [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}, {"id": 3, "name": "c"}, {"id": 4, "name": "d"}, {"id": 5, "name": "e"}]}
    '''
    if request.method == "GET":
        return get_method_error()

    try:
        response_data = list(EntityType.objects.all().values())
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="List entity type failed!",data=get_exception(e)))

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
        return get_method_error()

    body = json.loads(request.body)
    entity_type = body.get('type')

    try:
        records = EntityType(name=entity_type)
        records.save()
    except:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg='Add entity type failed!'))

    return JsonResponse(success_resp(msg=SAVE_SUCCESS_MSG))


def del_entity_type(request):
    '''
    删除实体类型,删除实体类型时会删除相应的打标数据，因为外键存在。
    判断删除tags后的sentence状态。
    filter筛选跟type有关的所有数据的tag_id 然后遍历,思考先删后删问题
    如果不考虑sentence状态，可能导致如下情况
     tag_type删除后，由于外键，同样会删除所关联tag的所有记录，如果某一个句子只有当前一个type，那么此时这个句子没有打标后的记录，但是同样不会被读入到实体打标中。
    如果先删，则无法通过 type -> tag_id -> sentence_id 从而无法更改sentence
    看来后删比较合适，但是同样存在更改标志位后该类型没有被删除的情况，不过只是被重新打标，影响可接受。
    :param request:
    {'id':int,'type':'f'}
    :return:
    {"success": true, "msg": "", "code": 0, "data":""}
    {'success':False,'msg':msg,'code':code,'data':data}
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    entity_id = int(body.get('id'))

    try:
        records = list(EntityTag.objects.filter(type__id=entity_id).all().values())
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Get tags by type failed!",data=get_exception(e)))

    if not records:
        return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE,msg="A wrong tag id"))

    for item in records:
        if not exist_sentence(item['id']):
            return JsonResponse(fail_resp(code=RECORD_NOT_EXIST_CODE, msg="This tag doesn't have relate sentence"))

    try:
        EntityType.objects.get(pk=entity_id).delete()
    except:
        return JsonResponse(fail_resp(code=DELETE_ERROR,msg='Delete entity type failed!'))

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
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    entity_id = int(body.get('id'))
    entity_type = body.get('type')

    try:
        records = EntityType.objects.get(pk=entity_id)
        records.name = entity_type
        records.save()
    except:
        return JsonResponse(fail_resp(code=SAVE_FAILED_CODE,msg=SAVE_FAILED_MSG))

    return JsonResponse(success_resp(msg="Edit entity type success!"))

# 判断当前数据库中是否还有当前的sentence_id，如果没有则需要更改sentence标志位。
# 考虑该操作放在删除前还是删除后？应该放在删除前，防止查询未成功但是删除数据的情况。
def exist_sentence(tag_id):
    try:
        num = EntityTag.objects.filter(sentence_id__id=tag_id).count()
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Get number of entity tags failed !",data=get_exception(e)))
    # 该 tag_id 不存在
    if num == 0 :
        return False

    # 只剩一条数据，此时更改标志位
    elif num == 1 :
        try:
            tag = EntityTag.objects.get(id=tag_id)

            sentence = Sentence(id=tag.sentence_id_id)
            sentence.entity_tag = False
            sentence.save()
        except Exception as e:
            return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Change sentence entity tag flag faild!",data=get_exception(e)))
        return True

    # 剩多条数据。
    else:
        return True
