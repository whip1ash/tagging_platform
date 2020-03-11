#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: urls.py.py
@time: 2020/3/10 20:50
@desc: entity web interface defination
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url('list',views.list_entity_type,name='List entity types.'),
    url('add',views.add_entity_type,name='Add entity types'),
    url('delete',views.del_entity_type,name='Delete entity types'),
    url('edit',views.edit_entity_type,name='Edit entity types')
]