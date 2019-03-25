# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-25 02:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0017_auto_20190106_0310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pause',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiments.Execution')),
            ],
        ),
        migrations.AlterField(
            model_name='latinsquare',
            name='row1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='row1_latin_square', to='experiments.LatinSquareRow'),
        ),
        migrations.AlterField(
            model_name='latinsquare',
            name='row2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='row2_latin_square', to='experiments.LatinSquareRow'),
        ),
    ]
