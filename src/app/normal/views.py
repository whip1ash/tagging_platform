# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import Sentence
from ..entity.models import EntityTag,EntityType
from ..relation.models import RelationTag,RelationType
from django.forms.models import model_to_dict

import json
import nltk
import re

def index(request):
    '''
    index 页面两个跳转，一个跳到实体打标，另一个跳到关系打标
    :param request:
    :return:
    '''
    return render(request, 'normal/index.html')


def page_not_found(request, exception):
    return render(request, 'normal/404.html')


def server_error(request):
    return render(request, 'normal/500.html')


def sentence_index(request):
    '''
    todo: 查看数据库中现存的句子。页面中发json，取历史记录到前端。
    :param request:
    :return:
    '''
    # todo: 新建html模板
    return render(request, 'sentence/index.html')


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

    offset = page2offset(page, limit)

    try:
        sentences = list(Sentence.objects.all()[offset:offset + limit].values())
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR, msg="List all sentence failed", data=get_exception(e)))

    return JsonResponse(success_resp(msg="List sentences success!", data=sentences))


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
            tagged_entities = queryset2list(Sentence.objects.filter(entity_tag=True).all()[offset:offset + limit])
        elif referer == "relation":
            tagged_entities = queryset2list(Sentence.objects.filter(relation_tag=True).all()[offset:offset + limit])
        elif referer == "all":
            tagged_entities = queryset2list(
                Sentence.objects.filter(entity_tag=True, relation_tag=True).all()[offset:offset + limit])
        else:
            return JsonResponse(fail_resp(code=WRONG_PARAM_CODE, msg="Input a invalid referer"))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR, msg="List done sentences failed!", data=get_exception(e)))

    return JsonResponse(success_resp(msg="List done sentences success!", data=tagged_entities))


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
            tagging_entities = queryset2list(
                Sentence.objects.exclude(entity_tag=True, relation_tag=True).all()[offset:limit])
        else:
            return JsonResponse(fail_resp(code=WRONG_PARAM_CODE, msg="Input a invalid referer"))
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
            done_num = Sentence.objects.filter(relation_tag=True, entity_tag=True).count()
            doing_num = all_num - done_num
        else:
            return JsonResponse(fail_resp(code=WRONG_PARAM_CODE, msg="Input a invalid referer"))
    except Exception as e:
        return JsonResponse(fail_resp(code=DATABASE_ERROR, msg="Count sencence failed!", data=get_exception(e)))

    return JsonResponse(
        success_resp(msg="Get sentence num success!", data={"doing_num": doing_num, "done_num": done_num}))


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
        return JsonResponse(fail_resp(code=DATABASE_ERROR, msg="Get a sentence failed!", data=get_exception(e)))

    return JsonResponse(success_resp(msg="Get a sentence success", data=sentence))


def export(request):
    '''
    todo: 数据导出功能，模块化拆出来。通过参数判断导出实体的数据还是关系的数据
    :param request:{'referer':'entity'}
    :return: xxx.txt
    '''
    entity_dict = {}
    tmp_sentence = queryset2list(Sentence.objects.all().values())
    for i in tmp_sentence:
        tmp_sen = Sen(i)
        if tmp_sen.entity:
            # storage format:{'id':int, 'word':word_content, 'label':'O'or"entity_type"}
            # split sentence(nltk.word_tokenize()) -> find sentence_id in tag table -> word[pos] : entity[entity_id]
            # sentence_id = i.get('id')

            # for j in tmp_spilt_sentence:
            #     tmp_word_dict = {'id': }
            #     entity_dict.add
            pass


class Sen:
    def __init__(self,tmp):
        '''
        初始化加载Sentence表中的当前行数据
        :param tmp: {'id':int,'content':str,'entity':bool,'relation':bool}
        '''
        self.id = tmp.get('id')
        self.content = tmp.get('content')
        self.entity = tmp.get('entity_tag')
        self.relation = tmp.get('relation_tag')

    def word_split(self,str):
        '''
        分割句子
        :param str: 'I am a man.'
        :return: ['I', 'am', 'a', 'man', '.']
        '''
        return nltk.word_tokenize(str)

    def find_entity_tag(self,sen_id):
        '''
        返回list类型的entity_tag表中符合sen_id的数据
        :param sen_id: int
        :return:[{'id':int,'pos':"x,y",'entity':str,'sentence_id':int,'type_id',int},...]
        '''
        return queryset2list(EntityTag.objects.filter(sentence_id=sen_id))

    def find_relation_tag(self,sen_id):
        '''
        返回list类型的relation_tag表中符合sen_id的数据
        :param sen_id: int
        :return:[{
    		"tag_id":int,
    		"sentence_id":int,
    		"head_entity_pos":"x(int),y(int)",
    		"head_entity":string,
    		"tail_entity_pos":"x(int),y(int)",
    		"tail_entity":string,
    		"type_id":int
		},...]
        '''
        return queryset2list(RelationTag.objects.filter(sentence_id=sen_id))

    def output_entity_training_data(self,sen,sen_id):
        splited_sen = self.word_split(sen)
        res = []
        count = 0
        tag_data = self.find_entity_tag(sen_id)
        entity_type = self.generate_printed_entity_type(tag_data,len(splited_sen))
        for i in splited_sen:
            count += 1
            tmp = {'id':self.id,'word':i,'type':entity_type[count-1]}
            res.append(tmp)
        return res

    def generate_printed_entity_type(self,tag_data,l):
        '''
        通过对生成第三列entity_type需要的数据
        :param tag_data:
        :param l:
        :return:
        '''
        res = ['O']*l
        for i in tag_data:
            tmp_pos = re.split(r'\W+',i.get('pos'))
            entity_id = i.get('type_id')
            res[tmp_pos[0]:tmp_pos[1]] = queryset2list(EntityTag.objects.get(pk=entity_id))[0].get('name')*(tmp_pos[1]-tmp_pos[0])
        return res



def queryset2list(queryset):
    res_list = list()
    for i in queryset:
        res_list.append(model_to_dict(i))

    return res_list
