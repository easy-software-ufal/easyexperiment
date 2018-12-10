# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from experiments.models import Participant, Experiment, Task, Execution

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class ExperimentAdmin(admin.ModelAdmin):
    inlines = [TaskInline,]
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('description', 'created_at', 'updated_at')

class ExperimentInline(admin.TabularInline):
    model = Experiment
    extra = 1
class ExecutionInline(admin.TabularInline):
    model = Execution
    readonly_fields = ('start', 'end',)
    extra = 1
class ParticipantAdmin(admin.ModelAdmin):
    inlines = [ExecutionInline,]
    list_filter = ('created_at',)

    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('name', 'email', 'created_at', 'updated_at')

admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Participant, ParticipantAdmin)
