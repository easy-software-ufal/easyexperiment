# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from experiments.models import Pause

class Command(BaseCommand):
    help = 'Fix wrong pauses'

    def handle(self, *args, **options):
        print [pause.id for pause in self.__pauses()]
        for pause in self.__pauses():
            print "ID: %d Duration: %f" % (pause.id, pause.duration_in_seconds())

    def __pauses(self):
        return Pause.objects.with_negative_duration()
