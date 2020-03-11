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
    url('ListType',views.list_entity_type(),name='List entity types.'),
    url('AddType',views.add_entity_type,name='Add entity types'),
    url('DelType',views.del_entity_type,name='Delete entity types'),
    url('EditType',views.edit_entity_type,name='Edit entity types'),
]