# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from experiments.models import Execution, Pause, Point, Task


class Command(BaseCommand):
    help = 'Analyse data for areas of interest'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.filter(experiment__id=4)

        for task in tasks:
            print "\n\n>> Analysing task %s" % task.description

            executions = Execution.objects.filter(task__id=task.id)
            total_points = 0

            for execution in executions:
                # print "Load points for execution %d" % execution.id

                points = Point.objects.filter(
                    datetime__range=(execution.start, execution.end),
                    y__gte=task.area_of_interest_points[0],
                    y__lte=task.area_of_interest_points[1]
                )

                # exclude pause points
                for pause in execution.pause_set.all():
                    points = points.exclude(datetime__range=(pause.start_time, pause.end_time))

                total_points += len(points)

            print total_points
