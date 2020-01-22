# -*- coding: utf-8 -*-

import csv

from django.core.management.base import BaseCommand
from django.db.models import Q

from experiments.models import LatinSquare, Execution


class Command(BaseCommand):
    help = 'Generate a new CSV file to be used as dataset on rstudio script'

    def handle(self, *args, **options):
        latin_squares = LatinSquare.objects.filter(experiment_id=3) \
                                           .exclude(Q(row1__participant_id__isnull=True) | Q(row2__participant_id__isnull=True))

        with open('C:/Users/nando/OneDrive/Documentos/datasetatoms_v2.csv', 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["", "Replica", "Id", "Student", "SetOfTasks", "Tasks", "Technique", "Trials", "Time", "Minutes"])

            for index, latin_square in enumerate(latin_squares, start=1):
                descriptions_row1_cell1 = [task.description for task in latin_square.row1.cell1.tasks.all()]
                tasks_row1_cell1 = ':'.join(descriptions_row1_cell1)
                descriptions_row1_cell2 = [task.description for task in latin_square.row1.cell2.tasks.all()]
                tasks_row1_cell2 = ':'.join(descriptions_row1_cell2)

                descriptions_row2_cell1 = [task.description for task in latin_square.row2.cell1.tasks.all()]
                tasks_row2_cell1 = ':'.join(descriptions_row2_cell1)
                descriptions_row2_cell2 = [task.description for task in latin_square.row2.cell2.tasks.all()]
                tasks_row2_cell2 = ':'.join(descriptions_row2_cell2)

                row1_cell1_type = ""
                row1_cell2_type = ""
                row2_cell1_type = ""
                row2_cell2_type = ""

                if latin_square.frame_sequence[:2] == [1,2]:
                    row1_cell1_type = "With Atom"
                    row1_cell2_type = "Without Atom"
                    row2_cell1_type = "Without Atom"
                    row2_cell2_type = "With Atom"
                else:
                    row1_cell1_type = "Without Atom"
                    row1_cell2_type = "With Atom"
                    row2_cell1_type = "With Atom"
                    row2_cell2_type = "Without Atom"

                # import code; code.interact(local=dict(globals(), **locals()))
                duration_row1_cell_1 = self.duration_for_cell(latin_square.row1.cell1, latin_square.row1.participant)
                duration_row1_cell_2 = self.duration_for_cell(latin_square.row1.cell2, latin_square.row1.participant)
                duration_row2_cell_1 = self.duration_for_cell(latin_square.row2.cell1, latin_square.row2.participant)
                duration_row2_cell_2 = self.duration_for_cell(latin_square.row2.cell2, latin_square.row2.participant)

                trials_row1_cell_1 = self.trials_for_cell(latin_square.row1.cell1, latin_square.row1.participant)
                trials_row1_cell_2 = self.trials_for_cell(latin_square.row1.cell2, latin_square.row1.participant)
                trials_row2_cell_1 = self.trials_for_cell(latin_square.row2.cell1, latin_square.row2.participant)
                trials_row2_cell_2 = self.trials_for_cell(latin_square.row2.cell2, latin_square.row2.participant)

                # write lines to csv        
                filewriter.writerow([index, latin_square.id, 1, latin_square.row1.participant.name.encode('utf-8'), "ST1", tasks_row1_cell1, row1_cell1_type, trials_row1_cell_1, duration_row1_cell_1, duration_row1_cell_1])
                filewriter.writerow([index, latin_square.id, 1, latin_square.row1.participant.name.encode('utf-8'), "ST2", tasks_row1_cell2, row1_cell2_type, trials_row1_cell_2, duration_row1_cell_2, duration_row1_cell_2])
                filewriter.writerow([index, latin_square.id, 2, latin_square.row2.participant.name.encode('utf-8'), "ST1", tasks_row2_cell1, row2_cell1_type, trials_row2_cell_1, duration_row2_cell_1, duration_row2_cell_1])
                filewriter.writerow([index, latin_square.id, 2, latin_square.row2.participant.name.encode('utf-8'), "ST2", tasks_row2_cell2, row2_cell2_type, trials_row2_cell_2, duration_row2_cell_2, duration_row2_cell_2])

    def executions_for_cell_and_participant(self, cell, participant):
        executions = []
        for task in cell.tasks.all():
            try:
                executions.append(Execution.objects.get(task=task, participant=participant))
            except:
                print "Não encontrou execution com a task {} e o participante {}".format(task.id, participant.id)

        return executions

    def duration_for_cell(self, cell, participant):
        total_duration = 0
        
        for execution in self.executions_for_cell_and_participant(cell, participant):
            total_duration += execution.duration_in_seconds()

        return total_duration


    def trials_for_cell(self, cell, participant):
        trials = 0

        for execution in self.executions_for_cell_and_participant(cell, participant):
            trials += execution.answer_set.all().count()

        return trials
