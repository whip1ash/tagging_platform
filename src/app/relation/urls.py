#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: urls.py.py
@time: 2020/3/10 19:36
@desc: relationship web interface defination
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url('list/',views.list_relation_type,name='List relation types.'),
    url('add/',views.add_relation_type,name='Add relation types'),
    url('delete/',views.del_relation_type,name='Delete relation types'),
    url('edit/',views.edit_relation_type,name='Edit relation types')
]