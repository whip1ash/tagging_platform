# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import Sentence
from django.forms.models import model_to_dict

import json

def index(request):
    '''
    index 页面两个跳转，一个跳到实体打标，另一个跳到关系打标
    :param request:
    :return:
    '''
    return render(request,'normal/index.html')

def page_not_found(request,exception):
    return render(request,'normal/404.html')

def server_error(request):
    return render(request,'normal/500.html')

def sentence_index(request):
    '''
    todo: 查看数据库中现存的句子。页面中发json，取历史记录到前端。
    :param request:
    :return:
    '''
    # todo: 新建html模板
    return render(request,'sentence/index.html')


def sentence_list(request):
    '''
    返回sentence表中的所有数据，记得分页
    {"page":int,"limit":int}
    :param request:
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    page = int(body.get("page")) if int(body.get("page")) > 0 else 0
    limit = int(body.get("limit")) if int(body.get("limit")) > 0 else 10

    offset = page2offset(page,limit)

    try:
        sentences = list(Sentence.objects.all()[offset:offset+limit].values())
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="List all sentence failed",data=get_exception(e)))

    return JsonResponse(success_resp(msg="List sentences success!",data=sentences))


def sentence_done(request):
    '''
    查看已打标的句子数据，判断来源，是entity、relation、all
    {"referer":entity,"page":int,"limit":int}
    :param request:
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    referer = body.get("referer")
    page = int(body.get("page")) if int(body.get("page")) > 0 else 0
    limit = int(body.get("limit"))

    offset = page2offset(page, limit)

    try:
        if referer == "entity":
            tagged_entities = queryset2list(Sentence.objects.filter(entity_tag=True).all()[offset:offset+limit])
        elif referer == "relation":
            tagged_entities = queryset2list(Sentence.objects.filter(relation_tag=True).all()[offset:offset+limit])
        elif referer == "all":
            tagged_entities = queryset2list(Sentence.objects.filter(entity_tag=True,relation_tag=True).all()[offset:offset+limit])
        else:
            return JsonResponse(fail_resp(code=WRONG_PARAM_CODE,msg="Input a invalid referer"))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="List done sentences failed!",data=get_exception(e)))

    return JsonResponse(success_resp(msg="List done sentences success!",data=tagged_entities))

def sentence_doing(request):
    '''
    查看正在打标中的数据，判断来源，entity、relation、all
    {"referer":entity}
    :param request:
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    referer = body.get("referer")
    page = int(body.get("page")) if int(body.get("page")) > 0 else 0
    limit = int(body.get("limit"))

    offset = page2offset(page, limit)

    try:
        if referer == "entity":
            tagging_entities = queryset2list(Sentence.objects.filter(entity_tag=False).all()[offset:limit])
        elif referer == "relation":
            tagging_entities = queryset2list(Sentence.objects.filter(relation_tag=False).all()[offset:limit])
        elif referer == "all":
            tagging_entities = queryset2list(Sentence.objects.exclude(entity_tag=True, relation_tag=True).all()[offset:limit])
        else:
            return JsonResponse(fail_resp(code=WRONG_PARAM_CODE,msg="Input a invalid referer"))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR, msg="List doing sentences failed!", data=get_exception(e)))

    return JsonResponse(success_resp(msg="List doing sentences success!", data=tagging_entities))


def sentence_count(request):
    '''
    返回句子的数量，同样判断三种来源情况。
    {"referer":entity}
    :param request:
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    referer = body.get("referer")

    try:
        if referer == "entity":
            doing_num = Sentence.objects.filter(entity_tag=False).count()
            done_num = Sentence.objects.filter(entity_tag=True).count()
        elif referer == "relation":
            doing_num = Sentence.objects.filter(relation_tag=False).count()
            done_num = Sentence.objects.filter(relation_tag=True).count()
        elif referer == "all":
            all_num = Sentence.objects.all().count()
            done_num = Sentence.objects.filter(relation_tag=True,entity_tag=True).count()
            doing_num = all_num - done_num
        else:
            return JsonResponse(fail_resp(code=WRONG_PARAM_CODE,msg="Input a invalid referer"))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Count sencence failed!",data=get_exception(e)))

    return JsonResponse(success_resp(msg="Get sentence num success!",data={"doing_num":doing_num,"done_num":done_num}))

def sentence_get(request):
    '''
    取一条未打标的数据，同样判断两种来源情况 entity/relation
    {"referer":entity}
    :param request:
    :return:
    '''
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    referer = body.get("referer")

    try:
        if referer == "entity":
            sentence = queryset2list(Sentence.objects.filter(entity_tag=False).all()[0:1])
        elif referer == "relation":
            sentence = queryset2list(Sentence.objects.filter(relation_tag=False).all()[0:1])
        else:
            return JsonResponse(fail_resp(code=WRONG_PARAM_CODE, msg="Input a invalid referer"))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR,msg="Get a sentence failed!",data=get_exception(e)))

    return JsonResponse(success_resp(msg="Get a sentence success",data=sentence))


def export(request):
    '''
    todo: 数据导出功能，模块化拆出来。通过参数判断导出实体的数据还是关系的数据
    :param request:
    :return:
    '''


def queryset2list(queryset):
    res_list = list()
    for i in queryset:
        res_list.append(model_to_dict(i))

    return res_list