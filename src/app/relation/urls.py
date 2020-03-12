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
    url('ListType',views.list_relation_type,name='List relation types.'),
    url('AddType',views.add_relation_type,name='Add relation types'),
    url('DelType',views.del_relation_type,name='Delete relation types'),
    url('EditType',views.edit_relation_type,name='Edit relation types'),
    url('Save',views.save,name='Save tags'),
    url('List',views.list_all,name='List History'),
    url('Count',views.count,name='Tags amount'),
    url('Del',views.delete,name='Delete specific tag'),
    url('Get',views.get,name='Get specific tag content')
]