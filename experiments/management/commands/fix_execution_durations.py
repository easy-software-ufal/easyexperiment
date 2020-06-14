# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from experiments.models import Execution


class Command(BaseCommand):
    help = 'Fix wrong executions'

    def handle(self, *args, **options):
        print [execution.id for execution in self.__executions()]
        for execution in self.__executions():
            print "%s %s" % (execution.start, execution.end)
            print "ID: %d Duration: %f Execution Total Duration: %f Pause Duration: %f" % (
                execution.id,
                execution.duration_in_seconds(),
                execution.execution_total_duration(),
                execution.pauses_duration()
            )

    def __executions(self):
        executions = Execution.objects.all()
        return filter(lambda execution: execution.duration_in_seconds() < 0, executions)
