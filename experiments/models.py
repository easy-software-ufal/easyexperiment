# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Experiment(models.Model):
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


def task_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/task_<id>/<filename>
    return 'uploads/task_{0}/{1}'.format(instance.user.id, filename)

class Task(models.Model):
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to=task_directory_path)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.description

class Execution(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Point(models.Model):
    x = models.CharField(max_length=200)
    y = models.CharField(max_length=200)
    datetime = models.DateTimeField(null=True, blank=True)
