# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import Group


class AuthGroupUrls(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    url = models.ForeignKey('AuthUrl', models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'auth_group_urls'
        unique_together = (('group', 'url'),)


class AuthUrl(models.Model):
    name = models.CharField(max_length=50)
    path = models.TextField(unique=True)
    element = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'auth_url'
