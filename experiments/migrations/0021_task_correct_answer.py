# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-04 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0020_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='correct_answer',
            field=models.CharField(default='', max_length=500),
        ),
    ]
