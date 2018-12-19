# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-10 05:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import experiments.models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0006_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to=experiments.models.task_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiment')),
            ],
        ),
        migrations.RemoveField(
            model_name='participant',
            name='end_datetime',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='flow',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='start_datetime',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='task1_data',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='task1_end',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='task1_start',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='task2_data',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='task2_end',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='task2_start',
        ),
        migrations.AddField(
            model_name='participant',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='participants',
            field=models.ManyToManyField(to='experiments.Participant'),
        ),
        migrations.AddField(
            model_name='execution',
            name='participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiments.Participant'),
        ),
        migrations.AddField(
            model_name='execution',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiments.Task'),
        ),
        migrations.AddField(
            model_name='participant',
            name='experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiment'),
        ),
    ]