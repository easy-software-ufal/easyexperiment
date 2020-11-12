# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from experiments.models import Execution, Point, Task
import time
import os


class Command(BaseCommand):
    help = 'Analyse data for areas of interest'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.filter(experiment__id=4)

        for task in tasks:
            print "\n\n>> Analysing task %s" % task.description

            executions = Execution.objects.filter(task__id=task.id)
            total_points = 0

            for execution in executions:
                print "Load points for execution %d" % execution.id
                points = Point.objects.filter(datetime__range=(execution.start, execution.end)).order_by('created_at')

                # exclude pause points
                for pause in execution.pause_set.all():
                    points = points.exclude(datetime__range=(pause.start_time, pause.end_time))

                total_points += len(points)

                # to_float = lambda x: float(x.replace(',', '.'))

                participant_id = execution.participant_id
                task_description = execution.task.description
                file_path = "/home/fernando/workspaces/ufal/exported_data/%d" % participant_id

                if not os.path.isdir(file_path):
                    os.mkdir(file_path)

                with open(os.path.join(file_path, "%s.csv" % task_description), 'w') as data_file:
                    data_file.write('x,y,time\n')
                    for point in points:
                        # timestamp = time.mktime(point.datetime.timetuple())
                        time = point.datetime.strftime('%H:%M:%S:%f')[:-3]
                        data_file.write("%s,%s,%s\n" % (point.x.replace(',', '.'), point.y.replace(',', '.'), time,))
