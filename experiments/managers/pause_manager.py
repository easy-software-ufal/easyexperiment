# -*- coding: utf-8 -*-

from django.db import models


class PauseManager(models.Manager):

    def with_negative_duration(self):
        from experiments.models import Pause
        pauses = Pause.objects.all()
        return filter(lambda pause: pause.duration_in_seconds() < 0, pauses)
