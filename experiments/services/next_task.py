# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
# pylint: disable=no-member
"""Search LatinSquare Row available"""
from django.db.models import Q
from experiments.models import LatinSquare


class NextTask(object):
    """Search the next task for a participant at an experiment"""

    SQL = """
        WITH cells_ids AS (
            SELECT id FROM experiments_latinsquarecell
                WHERE
                    experiments_latinsquarecell.id IN
                        (SELECT cell1_id FROM experiments_latinsquarerow
                            INNER JOIN experiments_latinsquare ON experiments_latinsquarerow.id IN(experiments_latinsquare.row1_id, experiments_latinsquare.row2_id)
                            WHERE participant_id = %d  and experiments_latinsquare.experiment_id = %d

                        ) OR
                    experiments_latinsquarecell.id IN
                        (SELECT cell2_id FROM experiments_latinsquarerow
                            INNER JOIN experiments_latinsquare ON experiments_latinsquarerow.id IN(experiments_latinsquare.row1_id, experiments_latinsquare.row2_id)
                            WHERE participant_id = %d and experiments_latinsquare.experiment_id = %d

                        )
                ORDER BY id DESC
        )
        SELECT DISTINCT experiments_task.* FROM experiments_task
            INNER JOIN experiments_latinsquarecell_tasks ON experiments_latinsquarecell_tasks.latinsquarecell_id IN(SELECT id FROM cells_ids)
            LEFT JOIN experiments_execution ON experiments_execution.participant_id = %d and experiments_execution.task_id = experiments_task.id
            WHERE
                experiments_task.id IN(experiments_latinsquarecell_tasks.task_id) and
                experiments_execution.id IS NULL

        ORDER BY id ASC
        LIMIT 1;
    """

    def __init__(self, experiment, participant):
        """Contructor"""
        self.experiment = experiment
        self.participant = participant

    def call(self):
        return self.__task()

    def __task(self):
        try:
            return Task.objects.raw(self.SQL % (participant.id, experiment.id, participant.id, experiment.id, participant.id,))[0]
        except IndexError:
            # Return None if the query result is empty
            return None
