from __future__ import unicode_literals
from django.db import models
class Messages(models.Model):
    id = models.BigAutoField(primary_key=True)
    sendId = models.BigIntegerField()
    sendName = models.CharField(max_length=60)
    recId = models.BigIntegerField()
    contents = models.CharField(max_length=300)
    readflag = models.SmallIntegerField(blank=True, null=True,default=0)
    updtime = models.DateTimeField()
    createtime = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'messages'


