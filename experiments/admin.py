# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from experiments.models import Participant

class ParticipantAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('name', 'email', 'created_at', 'updated_at')

admin.site.register(Participant, ParticipantAdmin)
