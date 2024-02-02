from django.db import models


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    body_original = models.TextField(blank=True, null=True)
    body_changed = models.TextField(blank=True, null=True)
