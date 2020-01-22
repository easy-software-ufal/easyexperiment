# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models

from experiments.managers.latin_square_manager import LatinSquareManager
from experiments.managers.pause_manager import PauseManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class Experiment(BaseModel):
    description = models.CharField(max_length=200)
    tasks_quantity_by_cell = models.IntegerField(
        default=1, blank=True, null=True
    )

    def __unicode__(self):
        return self.description


class Participant(BaseModel):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def finish_last_pause_for_each_execution(self):
        for execution in self.execution_set.all():
            last_pause = Pause.objects.filter(execution=execution) \
                              .order_by('-pk')

            if len(last_pause) > 0:
                last_pause = last_pause[0]
                if last_pause.end_time is None:
                    last_pause.end_time = datetime.now()
                    last_pause.save()

    # def finish_all_pauses(self):
    #    for execution in self.execution_set.all():
    #        execution.pause_set.all().update(end_time=datetime.now())

    def __unicode__(self):
        return self.name


class Task(BaseModel):
    FIRST_FRAME = 1
    SECOND_FRAME = 2
    THIRD_FRAME = 3
    FOURTH_FRAME = 4

    FRAME_CHOICES = (
        (FIRST_FRAME, 'Primeiro Quadrante'),
        (SECOND_FRAME, 'Segundo Quadrante'),
        (THIRD_FRAME, 'Terceiro Quadrante'),
        (FOURTH_FRAME, 'Quarto Quadrante'),
    )

    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/tasks')
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, blank=True, null=True
    )
    frame = models.IntegerField(choices=FRAME_CHOICES, blank=True, null=True)
    correct_answer = models.CharField(max_length=500, default='')

    def __unicode__(self):
        return self.description


def execution_plot_directory_path(instance, filename):
    return 'uploads/executions/heatmaps/{0}/{1}'.format(instance.id, filename)


class Execution(BaseModel):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, blank=True, null=True
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, blank=True, null=True
    )
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    number_of_errors = models.IntegerField(default=0)
    heatmap = models.ImageField(upload_to=execution_plot_directory_path,
                                blank=True, null=True, max_length=500)

    def pauses_duration(self):
        pauses_duration = 0
        for pause in self.pause_set.all():
            pauses_duration += pause.duration_in_seconds()

        return pauses_duration

    def execution_total_duration(self):
        if self.end is None or self.start is None:
            return 0

        return (self.end - self.start).total_seconds()

    def duration_in_seconds(self):
        return self.execution_total_duration() - self.pauses_duration()

    def duration_in_minutes(self):
        duration_in_s = self.duration_in_seconds()

        # duration_in_s = (self.end - self.start).total_seconds()

        # return divmod(duration_in_s, 60)[0]  # return in minutes
        return duration_in_s / 60


class Point(BaseModel):
    x = models.CharField(max_length=200)
    y = models.CharField(max_length=200)
    datetime = models.DateTimeField(null=True, blank=True)


class LatinSquareCell(BaseModel):
    tasks = models.ManyToManyField(Task)

    def __unicode__(self):
        return "%d" % self.id


class LatinSquareRow(BaseModel):
    cell1 = models.ForeignKey(
        LatinSquareCell, on_delete=models.CASCADE,
        blank=True, null=True, related_name='first_cell'
    )
    cell2 = models.ForeignKey(
        LatinSquareCell, on_delete=models.CASCADE,
        blank=True, null=True, related_name='second_cell'
    )
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE,
        blank=True, null=True, related_name='row_participant'
    )

    def __unicode__(self):
        return "%d" % self.id


class LatinSquare(BaseModel):
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, blank=True, null=True
    )
    row1 = models.OneToOneField(
        LatinSquareRow, on_delete=models.CASCADE,
        blank=True, null=True, related_name='row1_latin_square'
    )
    row2 = models.OneToOneField(
        LatinSquareRow, on_delete=models.CASCADE,
        blank=True, null=True, related_name='row2_latin_square'
    )
    frame_sequence = ArrayField(
        models.IntegerField(), null=True, blank=True, default=[1, 2, 3, 4]
    )

    objects = LatinSquareManager()

    def __unicode__(self):
        return "%d" % self.id


class Pause(BaseModel):
    execution = models.ForeignKey(
        Execution, on_delete=models.CASCADE, blank=True, null=True
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    objects = PauseManager()

    def duration_in_seconds(self):
        if self.end_time is None or self.start_time is None:
            return 0

        duration = self.end_time - self.start_time

        return duration.total_seconds()

    def __unicode__(self):
        return "%d %d" % (self.id, self.duration_in_seconds())


class Answer(BaseModel):
    execution = models.ForeignKey(Execution, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    correct = models.BooleanField()


class HeatMapFeedback(BaseModel):
    execution = models.ForeignKey('Execution', on_delete=models.CASCADE)
    corresponds_to_perception = models.BooleanField(default=True)
    notes = models.CharField(max_length=500)


class Survey(BaseModel):
    description = models.CharField(max_length=200)
    experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE)


class SurveyQuestion(BaseModel):
    INPUT_TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Text Area')
    )

    question = models.CharField(max_length=200)
    input_type = models.CharField(max_length=20, choices=INPUT_TYPE_CHOICES)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)


class SurveyAnswer(BaseModel):
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE)
    execution = models.ForeignKey('Execution', on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)


# from django.db.models.signals import post_save
#
# post_save.connect(handlers.my_handler, sender=LatinSquare)
