# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-19 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0010_auto_20181219_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latinsquare',
            name='row1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_row', to='experiments.LatinSquareRow'),
        ),
        migrations.AlterField(
            model_name='latinsquare',
            name='row2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_row', to='experiments.LatinSquareRow'),
        ),
    ]
