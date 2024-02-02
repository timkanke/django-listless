# Generated by Django 4.2.7 on 2023-12-27 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('body_original', models.TextField(blank=True, null=True)),
                ('body_changed', models.TextField(blank=True, null=True)),
            ],
        ),
    ]