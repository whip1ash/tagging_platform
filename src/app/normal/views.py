# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from ..utils.tools import *
from .models import Sentence
import json
from django.forms.models import model_to_dict

def index(request):
    """
    index 页面两个跳转，一个跳到实体打标，另一个跳到关系打标
    :param request:
    :return:
    """
    return render(request, 'normal/index.html')


def page_not_found(request, exception):
    return render(request, 'normal/404.html')


def server_error(request):
    return render(request, 'normal/500.html')


# todo: url这里添加新的路由:sentence
def sentence_index(request):
    """
    todo: 查看数据库中现存的句子。页面中发json，取历史记录到前端。
    :param request:
    :return:
    """
    # todo: 新建html模板
    return render(request, 'sentence/index.html')


def sentence_list(request):
    """
    todo: 返回sentence表中的所有数据，记得分页
    1k条，50条/页。1-20页，拟输入为1-20的整数
    若页数超过20给error？
    :param request: {'page':int}
    :return: 50条数据，包括{'id','content','source','entity_tag','relation_tag'}
    """
    if request.method == "GET":
        return get_method_error()

    body = json.loads(request.body)
    page_no = body.get('page')

    # try:
    list_data = list(Sentence.objects.all()[(page_no-1)*50:page_no*50])
    # except:
    #     return JsonResponse(fail_resp(code=))
    return JsonResponse(success_resp(msg="Get Sentence successful",data=list_data))


def sentence_done(request):
    """
    todo: 查看已打标的句子数据，判断来源，是entity、relation、all
    :param request:
    :return:
    """
    tagged_entity_data = model_to_dict(Sentence.objects.filter(entity_tag=True,relation_tag=False))
    tagged_relation_data = model_to_dict(Sentence.objects.filter(entity_tag=False,relation_tag=True))
    tagged_finished_data = model_to_dict(Sentence.objects.filter(entity_tag=True,relation_tag=True))

    return success_resp(msg='Judge finished',data={'entity':tagged_entity_data,'relation':tagged_relation_data,'all':tagged_finished_data})


def sentence_doing(request):
    """
    todo: 查看正在打标中的数据，判断来源，entity、relation、all
    :param request:
    :return:
    """



def sentence_count(request):
    '''
    todo: 返回句子的数量，同样判断三种来源情况。
    :param request:
    :return:{'success':True,'msg':msg,'code':0,'data':{'wiki data':wiki_source_data,'book data':book_source_data,'other source':other_source_data}}
    '''
    wiki_source_data = Sentence.objects.filter(source='W').count()
    book_source_data = Sentence.objects.filter(source='B').count()
    other_source_data = Sentence.objects.filter(source='O').count()

    return JsonResponse(success_resp(msg='Data source statics',data={'wiki data':wiki_source_data,'book data':book_source_data,'other source':other_source_data}))


def sentence_get(request):
    """
    todo: 取一条未打标的数据，同样判断两种来源情况 entity/relation
    :param request:
    :return:
    """



def export(request):
    """
    todo: 数据导出功能，模块化拆出来。通过参数判断导出实体的数据还是关系的数据
    :param request:
    :return:
    """
