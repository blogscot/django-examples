# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20160607_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateField(),
        ),
    ]