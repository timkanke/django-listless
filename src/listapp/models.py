from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    publish = models.BooleanField(null=True)
