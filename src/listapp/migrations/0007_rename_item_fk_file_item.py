# Generated by Django 4.2.7 on 2023-11-22 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0006_remove_item_file_fk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='item_fk',
            new_name='item',
        ),
    ]
