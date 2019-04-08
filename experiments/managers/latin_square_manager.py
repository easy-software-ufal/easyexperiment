# -*- coding: utf-8 -*-

import random

from django.db import models


class LatinSquareManager(models.Manager):

    def create_with_rows(self, experiment):
        from experiments.models import LatinSquare
        latin_square = LatinSquare.objects.create(
            experiment=experiment,
            frame_sequence=self.__generate_frame_sequence()
        )
        from experiments.services.generate_latin_square_rows import GenerateLatinSquareRows
        GenerateLatinSquareRows(latin_square).call()

        return latin_square

    def __generate_frame_sequence(self):
        shuffled = [[1, 2], [3, 4]]
        random.shuffle(shuffled)
        return shuffled[0] + shuffled[1]
