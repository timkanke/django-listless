# Generated by Django 4.2.7 on 2023-11-27 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0007_rename_item_fk_file_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='item',
        ),
        migrations.AddField(
            model_name='item',
            name='files',
            field=models.ManyToManyField(to='listapp.file'),
        ),
    ]
