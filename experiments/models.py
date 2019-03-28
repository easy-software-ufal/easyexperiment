# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Experiment(models.Model):
    description = models.CharField(max_length=200)
    tasks_quantity_by_cell = models.IntegerField(default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.description

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Task(models.Model):
    COMMON = 1
    SPECIAL = 2
    KIND_CHOICES = (
        (COMMON, 'Common'),
        (SPECIAL, 'Special'),
    )

    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'uploads/tasks')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    kind = models.IntegerField(choices=KIND_CHOICES, blank=True, null=True)
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
    number_of_errors = models.IntegerField(default=0)


class Point(models.Model):
    x = models.CharField(max_length=200)
    y = models.CharField(max_length=200)
    datetime = models.DateTimeField(null=True, blank=True)


class LatinSquareCell(models.Model):
    tasks = models.ManyToManyField(Task)

    def __unicode__(self):
        return "%d" % self.id


class LatinSquareRow(models.Model):
    cell1 = models.ForeignKey(LatinSquareCell, on_delete=models.CASCADE, blank=True, null=True, related_name='first_cell')
    cell2 =  models.ForeignKey(LatinSquareCell, on_delete=models.CASCADE, blank=True, null=True, related_name='second_cell')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, blank=True, null=True, related_name='row_participant')

    def __unicode__(self):
        return "%d" % self.id

class LatinSquare(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    row1 = models.ForeignKey(LatinSquareRow, on_delete=models.CASCADE, blank=True, null=True, related_name='row1_latin_square')
    row2 = models.ForeignKey(LatinSquareRow, on_delete=models.CASCADE, blank=True, null=True, related_name='row2_latin_square')

    def __unicode__(self):
        return "%d" % self.id

class Pause(models.Model):
    execution = models.ForeignKey(Execution, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def duration_in_seconds(self):
        duration = self.end_time - self.start_time

        return duration.total_seconds()

# from django.db.models.signals import post_save
from experiments.signals import handlers

# post_save.connect(handlers.my_handler, sender=LatinSquare)
