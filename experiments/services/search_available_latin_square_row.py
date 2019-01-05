# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
# pylint: disable=no-member
"""Search LatinSquare Row available"""
from django.db.models import Q
from experiments.models import LatinSquare


class SearchAvailableLatinSquareRow(object):
    """Serch the first LatinSquareRow available for a participant"""

    SQL = """
        SELECT experiments_latinsquare.id, experiments_latinsquare.experiment_id, experiments_latinsquare.row1_id, experiments_latinsquare.row2_id FROM experiments_latinsquare
        INNER JOIN experiments_latinsquarerow ON experiments_latinsquarerow.id IN(experiments_latinsquare.row1_id, experiments_latinsquare.row2_id)
        LEFT JOIN experiments_participant ON experiments_participant.id = experiments_latinsquarerow.participant_id
        WHERE
            experiments_latinsquare.experiment_id = %d AND
            experiments_latinsquarerow.participant_id IS NULL
        LIMIT 1;
    """

    def __init__(self, experiment):
        """Contructor"""
        self.experiment = experiment

    def call(self):
        latin_square = LatinSquare.objects.raw(self.SQL % self.experiment.id)[0]

        if latin_square is not None:
            return latin_square.row1 if latin_square.row1.participant is None else latin_square.row2
        else:
            return None
