# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from experiments.models import Participant

class ParticipantAdmin(admin.ModelAdmin):
    pass

admin.site.register(Participant, ParticipantAdmin)