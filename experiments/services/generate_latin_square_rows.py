# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
# pylint: disable=no-member
"""Generate latin square rows when a latin square is created"""
from experiments.models import Task, LatinSquareCell, LatinSquareRow


class GenerateLatinSquareRows(object):
    """Generate Latin Square Rows"""

    def __init__(self, latin_square):
        self.latin_square = latin_square

    def call(self):
        """Constructor"""
        if not self.latin_square.row1 or not self.latin_square.row2:
            self.__create_rows()

    # PRIVATE METHODS
    def __random_tasks_for_frame(self, frame):
        """Get tasks randomly based on frame"""
        return Task.objects \
            .filter(frame=frame, experiment_id=self.latin_square.experiment.id) \
            .exclude(id__in=self.__tasks_to_exclude())

    def __create_rows(self):
        """Create rows for current latin square"""
        cells = self.__create_cells()

        self.latin_square.row1 = LatinSquareRow.objects.create(
            cell1=cells[:2][0],
            cell2=cells[:2][1]
        )

        self.latin_square.row2 = LatinSquareRow.objects.create(
            cell1=cells[2:][0],
            cell2=cells[2:][1]
        )

        self.latin_square.save()

    def __create_cells(self):
        """create cells to latin square"""
        cells = []

        for frame in self.latin_square.frame_sequence:
            cell = LatinSquareCell.objects.create()
            cell.tasks = self.__random_tasks_for_frame(frame)
            cell.save()
            cells.append(cell)

        return cells

    def __tasks_to_exclude(self):
        """get all tasks already at the current latin square to not repeat then"""
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
