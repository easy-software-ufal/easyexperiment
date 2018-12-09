# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from experiments.models import Participant

class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ('start_datetime',)
    list_display = ('name', 'email', 'start_datetime', 'end_datetime', 'task1_start', 'task1_end', 'task2_start', 'task2_end')

admin.site.register(Participant, ParticipantAdmin)