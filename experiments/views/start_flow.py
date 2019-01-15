# -*- coding: utf-8 -*-
"""First screen of experiment flow"""

from django.http import HttpResponse
from django.views.generic.edit import FormView
from experiments.forms import ParticipantForm

class StartFlow(FormView):
    template_name = 'start_flow.html'
    form_class = ParticipantForm
    success_url = '/experiments/next-task/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(StartFlow, self).get_initial()

        initial['experiment_id'] = self.kwargs['experiment_id']

        return initial

    def form_valid(self, form):
        participant = form.save_participant()
        experiment  = self.__experiment_from_participant(participant)
        self.success_url += '%d/%d/' % (participant.id, experiment.id)
        return super(StartFlow, self).form_valid(form)


    def __experiment_from_participant(self, participant):
        latin_square = participant.row_participant.first().row1_latin_square.first()

        if latin_square is None:
            latin_square = participant.row_participant.first().row2_latin_square.first()

        return latin_square.experiment
