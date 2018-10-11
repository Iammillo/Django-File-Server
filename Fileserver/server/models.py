from django.db import models


class DBase(models.Model):
    Tag=models.CharField(max_length=30)
    Author=models.CharField(max_length=30)
    File=models.FileField()
    Ext=models.CharField(max_length=10, default=" ")
