# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
class Works(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    workname = models.CharField(max_length=60)
    typeoneid = models.BigIntegerField()
    typetwoid = models.BigIntegerField()
    label = models.CharField(max_length=60)
    licensetype = models.SmallIntegerField(default=0)
    introduce = models.CharField(max_length=300)
    firstmsg = models.CharField(max_length=300)
    chaptname = models.CharField(max_length=240, blank=True, null=True)
    curchapte = models.BigIntegerField(default=0)
    pubflag = models.SmallIntegerField(default=0)
    finishflag = models.SmallIntegerField(default=0)
    cnum = models.IntegerField(default=0)
    updtime = models.DateTimeField()
    createtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'works'


class Worktypeone(models.Model):
    id = models.BigAutoField(primary_key=True)
    typename = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'worktypeone'


class Worktypetwo(models.Model):
    id = models.BigAutoField(primary_key=True)
    typename = models.CharField(max_length=60)
    oneid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'worktypetwo'

