# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import Sentence
from django.forms.models import model_to_dict
from app.entity.models import EntityType,EntityTag
from app.relation.models import RelationType,RelationTag

from pandas import DataFrame
import pandas as pd
import json
import nltk
import re

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
    :param request:
    :return:
    '''

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
            tagging_entities = queryset2list(Sentence.objects.filter(entity_tag=False).all()[offset:offset+limit])
        elif referer == "relation":
            tagging_entities = queryset2list(Sentence.objects.filter(relation_tag=False).all()[offset:offset+limit])
        elif referer == "all":
            tagging_entities = queryset2list(Sentence.objects.exclude(entity_tag=True, relation_tag=True).all()[offset:offset+limit])
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


# 这里删除句子有一个问题，在关系打标中删除该句子，由于关联外键，那么实体打标中与该句话有关的数据会被删除。
def sentence_delete(request):
    if request.method == "GET":
        return get_method_error()
    body = json.loads(request.body)
    sen_id  = body.get("id")

    try:
        Sentence.objects.get(pk=sen_id).delete()
    except:
        return JsonResponse(fail_resp(code=DELETE_ERROR,msg='Delete Sentence failed!'))

    return JsonResponse(success_resp(msg="Delete Sentence success!"))

def export(request):
    '''
    todo: 数据导出功能，模块化拆出来。通过参数判断导出实体的数据还是关系的数据
    :param request:
    :return:
    '''
    data = []
    body = json.loads(request.body)
    referer = body.get("referer")
    tmp_sentence = queryset2list(Sentence.objects.all())
    for i in tmp_sentence:
        tmp_sen = Sen(i)
        if (tmp_sen.entity and referer == 'entity'):
            # storage format:{'id':int, 'word':word_content, 'label':'O'or"entity_type"}
            # split sentence(nltk.word_tokenize()) -> find sentence_id in tag table -> word[pos] : entity[entity_id]
            data.append(tmp_sen.output_entity_training_data(tmp_sen.content, tmp_sen.id))
        elif (tmp_sen.relation and referer == 'relation'):
            data.append(tmp_sen.output_relation_training_data(tmp_sen.content, tmp_sen.id))
        else:
            pass

    tmp_sen.print_into_file(referer, data)
    return JsonResponse(success_resp(msg="Export data success!"))


class Sen:
    def __init__(self, tmp):
        '''
        初始化加载Sentence表中的当前行数据
        :param tmp: {'id':int,'content':str,'entity':bool,'relation':bool}
        '''
        self.id = tmp.get('id')
        self.content = tmp.get('content')
        self.entity = tmp.get('entity_tag')
        self.relation = tmp.get('relation_tag')

    def word_split(self, content):
        '''
        分割句子
        :param content: 'I am a man.'
        :return: ['I', 'am', 'a', 'man', '.']
        '''
        return nltk.word_tokenize(content)

    def find_entity_tag(self, sen_id):
        '''
        返回list类型的entity_tag表中符合sen_id的数据
        :param sen_id: int
        :return:[{'id':int,'pos':"x,y",'entity':str,'sentence_id':int,'type_id',int},...]
        '''
        try:
            if EntityTag.objects.filter(sentence_id=sen_id) != None:
                return queryset2list(EntityTag.objects.filter(sentence_id=sen_id))
        except e:
            print("No tagged entity in this Sentence")

    def find_relation_tag(self, sen_id):
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
        try:
            if EntityTag.objects.filter(sentence_id=sen_id) != None:
                return queryset2list(RelationTag.objects.filter(sentence_id=sen_id))
        except e:
            print("No tagged relation in this Sentence")

    @staticmethod
    def dataframe_initialize():
        '''
        初始化DataFrame
        :return: 初始化好的dataframe，具有有顺序的3列id/word/type
        '''
        tmp = pd.DataFrame(columns={'id','word','type'})
        tmp['id'] = tmp['id'].apply(pd.to_numeric)
        tmp = tmp[['id','word','type']]
        return tmp

    def output_entity_training_data(self, sen, sen_id):
        '''
        生成输出需要的三列各自的数据
        :param sen: str(句子)
        :param sen_id: sentence_id
        :return: [{'id': int, 'word': str, 'type': str},...]
        '''
        splited_sen = self.word_split(sen)
        res = []
        count = 0
        tag_data = self.find_entity_tag(sen_id)
        entity_type = self.generate_printed_entity_type(tag_data, len(splited_sen))
        for i in splited_sen:
            count += 1
            tmp = {'id': self.id, 'word': i, 'type': entity_type[count - 1]}
            res.append(tmp)
        return res

    def generate_printed_entity_type(self, tag_data, l):
        '''
        通过对生成第三列entity_type需要的数据
        :param tag_data: 符合sentence_id的打标数据
        :param l: 句子包含的词及标点的个数
        :return:
        '''
        res = ['O'] * l
        for i in tag_data:
            tmp_pos = self.get_pos(i.get('pos'))
            entity_id = i.get('type')
            type_name =queryset2list(EntityType.objects.filter(pk=i.get('type')))[0].get('name')
            count  = tmp_pos[1] - tmp_pos[0] + 1
            B_label = 1
            while count :
                if B_label and count > 1:
                    res[tmp_pos[0]+count-1] = 'B-' + type_name
                    B_label = B_label - 1
                else:
                    res[tmp_pos[0]+count-1] = 'I-' + type_name
                count = count - 1
        return res

    def output_relation_training_data(self, sen, sen_id):
        '''
        :param sen:
        :param sen_id:
        :return:
        '''
        splited_sen = self.word_split(sen)
        res = []
        count = 0
        tag_data = self.find_relation_tag(sen_id)
        tmp = self.generate_printed_relation_type(tag_data, splited_sen)
        res.append(tmp)
        return res

    def generate_printed_relation_type(self, tag_data, splited_sen):
        '''
        通过对生成第三列entity_type需要的数据
        :param tag_data: 符合sentence_id的打标数据
        :param splited_sen: 分割后的句子
        :return
        '''
        token = splited_sen
        h = {"name": tag_data[0].get('head_entity'), "pos": self.get_pos(tag_data[0].get('head_entity_pos'))}
        t = {"name": tag_data[0].get('tail_entity'), "pos": self.get_pos(tag_data[0].get('tail_entity_pos'))}
        relation = queryset2list(RelationType.objects.filter(pk=tag_data[0].get('type')))[0].get('name')
        res = {"token": token, "h": h, "t": t, "relation": relation}
        return res

    @staticmethod
    def get_pos(str):
        '''
        格式化'pos'
        :param self:
        :param str:"1,2"
        :return: [1,2]
        '''
        tmp = re.split(r'\W+', str)
        res = []
        for i in tmp:
            res.append(int(i))
        return res

    def print_into_file(self, referer, data):
        '''
        输出到文件
        :param referer:"entity"
        :param data: {"id":int,...}
        :return: None
        '''
        if referer == 'entity':
            df = self.dataframe_initialize()
            df = df.append(data[0],ignore_index=True)
            print(df)
            df.to_csv("/root/school/data/train_entity.csv")
        elif referer == 'relation':
            fo = open("/root/school/data/train_relation.json", "a+")
            relation_data = data
            for i in relation_data:
                fo.write(str(i)+'\n')
            fo.close()
        else:
            print("param error")


def queryset2list(queryset):
    res_list = list()
    for i in queryset:
        res_list.append(model_to_dict(i))

    return res_list