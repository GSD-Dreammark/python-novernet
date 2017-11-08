# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=60)
    pwd = models.CharField(max_length=60)
    nicheng = models.CharField(unique=True, max_length=60)
    createtime = models.DateTimeField()
    # ?
    role = models.SmallIntegerField(default=1)
    msgnum = models.BigIntegerField(default=0)
    updtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
