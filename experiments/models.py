# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    flow = models.CharField(max_length=200)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    task1_start = models.DateTimeField(null=True, blank=True)
    task1_end = models.DateTimeField(null=True, blank=True)
    task2_start = models.DateTimeField(null=True, blank=True)
    task2_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name