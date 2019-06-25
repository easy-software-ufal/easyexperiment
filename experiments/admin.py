# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html

from experiments.models import Participant, Experiment, Task, Execution, Point, LatinSquare, LatinSquareRow

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class ExperimentInline(admin.TabularInline):
    model = Experiment
    extra = 1


class ExecutionInline(admin.TabularInline):
    model = Execution
    readonly_fields = ('start', 'end',)
    extra = 1


class LatinSquareRowInline(admin.TabularInline):
    model = LatinSquareRow
    extra = 1


class ExperimentAdmin(admin.ModelAdmin):
    inlines = [TaskInline,]
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('description', 'created_at', 'updated_at')


class TaskAdmin(admin.ModelAdmin):
    inlines = [ExecutionInline,]
    list_filter = ('created_at', 'experiment',)
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('description', 'image', 'experiment', 'created_at', 'updated_at')


class ParticipantAdmin(admin.ModelAdmin):
    inlines = [ExecutionInline,]
    list_filter = ('created_at',)

    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('name', 'email', 'created_at', 'updated_at')


class ExecutionAdmin(admin.ModelAdmin):
    list_filter = ('participant', 'task', 'start', 'end', 'created_at', 'updated_at',)
    readonly_fields = ('start', 'end', 'created_at', 'updated_at',)
    list_display = ('participant', 'task', 'start', 'end', 'created_at', 'updated_at',)


class PointAdmin(admin.ModelAdmin):
    readonly_fields = ('x', 'y', 'datetime',)
    list_display = ('x', 'y', 'datetime',)
    list_filter = ('datetime',)


class LatinSquareAdmin(admin.ModelAdmin):
    list_filter = ('experiment', 'row1', 'row2',)
    readonly_fields = ('row1', 'row2',)
    list_display = ('id', 'experiment',)

admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(LatinSquare, LatinSquareAdmin)
