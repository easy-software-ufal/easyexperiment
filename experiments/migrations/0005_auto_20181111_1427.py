# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-11 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0004_auto_20181109_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='task1_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='task2_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
