from django.db import models
from django.utils.translation import gettext_lazy as _

import pathlib


class File(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    file = models.FileField(upload_to='files')

    def extension(self):
        extension = pathlib.Path(self.file.file).suffix
        if extension == 'jpg':
            return 'jpg'
        if extension == 'jpeg':
            return 'jpeg'
        if extension == 'png':
            return 'png'
        if extension == 'pdf':
            return 'pdf'
        if extension == 'docx':
            return 'docx'
        return 'other'


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    publish = models.BooleanField(null=True)
    files = models.ManyToManyField(File)


class Image(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='pics')


class Cat(models.Model):
    class Gender(models.TextChoices):
        FEMALE = 'F', _('Female')
        MALE = 'M', _('Male')
        UNKNOWN = 'U', _('Unknown')

    name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=Gender.choices, blank=False, default='U')
    age = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    breed = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='cat', blank=True, null=True)
