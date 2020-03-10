# coding: utf-8

from django.db import models
from ..normal.models import Sentence

class EntityType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Entity Type",max_length=1024)

    def __str__(self):
        return self.name

class EntityTag(models.Model):
    # Auto Filed will added by Django automaticly
    id = models.AutoField(primary_key=True)
    # 对Django外键不理解的看这里 https://zhuanlan.zhihu.com/p/25393972
    sentence_id = models.ForeignKey(Sentence,on_delete=models.CASCADE,to_field='id',verbose_name="Tag Related Sentence Id")
    # Tag Position
    pos = models.CharField(verbose_name="Tag Position",max_length=20)
    # Entity Tag Content
    entity = models.CharField(verbose_name="Entity Tag Content",max_length=1024)
    # Entity Tag Type
    # 这里挂外键，当类型删除的时候删除所有记录
    type = models.ForeignKey(EntityType,on_delete=models.CASCADE,to_field='id',verbose_name="Entity Tag Type")

