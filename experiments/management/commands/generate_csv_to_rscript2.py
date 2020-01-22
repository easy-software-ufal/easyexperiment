# -*- coding: utf-8 -*-

import csv
from django.core.management.base import BaseCommand
from django.db.models import Q
from experiments.models import LatinSquare, Execution


class Command(BaseCommand):
    help = 'Generate a new CSV file to be used as dataset on rstudio script'

    def handle(self, *args, **options):
        executions = Execution.objects\
                        .filter(task__experiment_id=3)\
                        .exclude(participant_id=18).order_by('-id') # O eye tracker não funcionou na aplicação da Lettícia


        with open('C:/Users/nando/workspaces/ufal/Atoms-of-Confusion-Experiment-Analysis/pilot2-data.csv', 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["", "Replica", "Id", "Student", "SetOfTasks", "Tasks", "Technique", "Trials", "Time", "Minutes"])

            for index, execution in enumerate(executions, start=1):
                if hasattr(execution.participant.row_participant, 'row1_latin_square'):
                    latin_square = execution.participant.row_participant.row1_latin_square
                    idline = 1
                else:
                    latin_square = execution.participant.row_participant.row2_latin_square
                    idline = 2

                set_of_tasks = "ST1" if execution.task.frame in [1,3] else "ST2"

                tasks = execution.task.description.split('.')[0]

                if execution.task.description.endswith(".1"):
                    technique = "With Atom"
                else:
                    technique = "Without Atom"

                filewriter.writerow(
                    [
                        index,
                        latin_square.id,
                        idline,
                        execution.participant.name.encode('utf-8'),
                        set_of_tasks,
                        tasks,
                        technique,
                        execution.answer_set.all().count(),
                        int(execution.duration_in_seconds() * 60000),
                        execution.duration_in_minutes()
                    ]
                )
