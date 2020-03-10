from django.db import models
from ..normal.models import Sentence

class RelationType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Relation Type",max_length=1024)

    def __str__(self):
        return self.name

class RelationTag(models.Model):
    # Auto Filed will added by Django automaticly
    id = models.AutoField(primary_key=True)
    # 参考 app.entity.models.EntityTag
    sentence_id = models.ForeignKey(Sentence,on_delete=models.CASCADE,to_field='id',verbose_name="Tag Related Sentence Id")
    head_entity = models.CharField(verbose_name="Head Entity Content",max_length=1024)
    head_entity_pos = models.CharField(verbose_name="Head Entity Position",max_length=20)
    tail_entity = models.CharField(verbose_name="Tail Entity Content",max_length=1024)
    tail_entity_pos = models.CharField(verbose_name="Tail Entity Postion",max_length=20)
    type = models.ForeignKey(RelationType,on_delete=models.CASCADE,to_field='id',verbose_name="Relation Tag Type")