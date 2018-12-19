# -*- coding: utf-8 -*-
from experiments.models import Task, LatinSquareCell, LatinSquareRow, LatinSquare

class GenerateLatinSquareRows:
    def __init__(self, latin_square):
        self.latin_square = latin_square

    def call(self):
        if not self.latin_square.row1 or not self.latin_square.row2:
            self.__create_rows()

    # PRIVATE METHODS
    def __random_tasks_by_kind(self, kind):
        return Task.objects\
                   .filter(kind=kind)\
                   .exclude(id__in=self.__tasks_to_exclude())\
                   .order_by('?')[:self.latin_square.tasks_quantity_by_cell]

    def __create_rows(self):
        first_row_cells = self.__create_cells()
        self.latin_square.row1 = LatinSquareRow.objects.create(cell1=first_row_cells['common_cell'], cell2=first_row_cells['special_cell'])

        second_row_cells = self.__create_cells()
        self.latin_square.row2 = LatinSquareRow.objects.create(cell1=second_row_cells['special_cell'], cell2=second_row_cells['common_cell'])

        self.latin_square.save()


    def __create_cells(self):
        common_cell = LatinSquareCell.objects.create()
        common_cell.tasks = self.__random_tasks_by_kind(Task.COMMON)
        common_cell.save()

        special_cell = LatinSquareCell.objects.create()

        # tasks_to_exclude = list(map(lambda x: x.id, common_cell.tasks.all()))
        special_cell.tasks = self.__random_tasks_by_kind(Task.SPECIAL)
        special_cell.save()

        return {
            'common_cell': common_cell,
            'special_cell': special_cell
        }

    def __tasks_to_exclude(self):
        rows = [self.latin_square.row1, self.latin_square.row2]

        cells = []
        for row in rows:
            if row:
                cells += [row.cell1, row.cell2]

        tasks_to_exclude = []
        for cell in cells:
            for task in cell.tasks.all():
                tasks_to_exclude.append(task.id)

        return tasks_to_exclude
