# Generated by Django 4.2.7 on 2024-05-17 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listapp", "0009_cat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cat",
            name="gender",
            field=models.CharField(
                choices=[("F", "Female"), ("M", "Male"), ("U", "Unknown")],
                default="U",
                max_length=50,
            ),
        ),
    ]