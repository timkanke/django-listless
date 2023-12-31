# Generated by Django 4.2.7 on 2023-11-21 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0002_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('file', models.FileField(upload_to='files')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listapp.item')),
            ],
        ),
    ]
