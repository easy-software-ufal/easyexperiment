# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-02 04:05
from __future__ import unicode_literals

from django.db import migrations, models
import experiments.models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0028_auto_20191128_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution',
            name='heatmap',
            field=models.ImageField(blank=True, null=True, upload_to=experiments.models.execution_plot_directory_path),
        ),
    ]
