from django.db import models

class Sentence(models.Model):
    SENTENCE_SOURCE = [
        ('W','wiki'),
        ('B','book'),
        ('O','others')
    ]

    # Auto Filed will added by Django automaticly
    id = models.AutoField(primary_key=True)
    # Sentence Content
    content = models.CharField(verbose_name="Sentence Content",max_length=2048,)
    # Sentence Source
    source = models.CharField(verbose_name="Snetence Source",max_length=64,choices=SENTENCE_SOURCE)
    # Entity Tag Flag
    entity_tag = models.BooleanField("Entity Tag Flag",default=False)
    # Relation Tag Flag
    relation_tag = models.BooleanField("Relation Tag Flag",default=False)
