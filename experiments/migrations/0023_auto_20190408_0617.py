# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-08 06:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0022_auto_20190408_0505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='latinsquare',
            old_name='quadrant_sequence',
            new_name='frame_sequence',
        ),
    ]
