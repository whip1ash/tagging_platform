# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

from app.utils.tools import *
from .models import RelationTag,RelationType

def list_relation_type(request):
    response_data = list(RelationType.object.all().value())
    return JsonResponse(success_resp(data=response_data))

def add_relation_type(request):
    pass

def del_relation_type(request):
    pass

def edit_relation_type(request):
    pass
