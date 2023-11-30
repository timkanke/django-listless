from django.db import models

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
