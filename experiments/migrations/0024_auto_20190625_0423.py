# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-25 04:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0023_auto_20190408_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latinsquare',
            name='row1',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='row1_latin_square', to='experiments.LatinSquareRow'),
        ),
        migrations.AlterField(
            model_name='latinsquare',
            name='row2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='row2_latin_square', to='experiments.LatinSquareRow'),
        ),
    ]
