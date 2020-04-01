#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: urls.py.py
@time: 2020/3/10 20:50
@desc:
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url('List',views.sentence_list,name='List sentences.'),
    url('Done',views.sentence_done,name='List done sentences'),
    url('Doing',views.sentence_doing,name="List doing sentences"),
    url('Count',views.sentence_count,name="Get the number of sentences"),
    url('Get',views.sentence_get,name="Get a untagged sentence"),
    url('Export',views.export,name="Export data"),
    url('Del', views.sentence_delete, name="Delete the sentnece which don't have entity")

]