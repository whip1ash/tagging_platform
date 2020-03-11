# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *

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

# todo: url这里添加新的路由:sentence
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
    todo: 返回sentence表中的所有数据，记得分页
    :param request:
    :return:
    '''
    pass

def sentence_done(request):
    '''
    todo: 查看已打标的句子数据，判断来源，是entity、relation、all
    :param request:
    :return:
    '''

    pass

def sentence_doing(request):
    '''
    todo: 查看正在打标中的数据，判断来源，entity、relation、all
    :param request:
    :return:
    '''

    pass

def sentence_count(request):
    '''
    todo: 返回句子的数量，同样判断三种来源情况。
    :param request:
    :return:
    '''
    pass

def sentence_get(request):
    '''
    todo: 取一条未打标的数据，同样判断三种来源情况
    :param request:
    :return:
    '''

def export(request):
    '''
    todo: 数据导出功能，模块化拆出来。通过参数判断导出实体的数据还是关系的数据
    :param request:
    :return:
    '''