# -*- coding: utf-8 -*-

from datetime import datetime
from django import forms
from experiments.models import Experiment, LatinSquare, Participant
from experiments.services.search_available_latin_square_row import SearchAvailableLatinSquareRow

class ParticipantForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(help_text='A valid email address, please.')
    experiment_id = forms.IntegerField(widget = forms.HiddenInput(), required = True)

    def save_participant(self):
        name          = self.cleaned_data['name']
        email         = self.cleaned_data['email']
        experiment_id = self.cleaned_data['experiment_id']
        experiment    = self.__experiment(experiment_id)

        participant = Participant.objects.create(name = name, email = email)

        latin_square_row = SearchAvailableLatinSquareRow(experiment).call()

        if latin_square_row is not None:
            latin_square_row.participant = participant
            latin_square_row.save()
        else:
            latin_square = LatinSquare.objects.create(experiment = experiment)
            latin_square.row1.participant = participant
            latin_square.row1.save()

        return participant

    def __experiment(self, experiment_id):
        return Experiment.objects.get(pk=experiment_id)
