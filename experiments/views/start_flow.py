# -*- coding: utf-8 -*-
"""First screen of experiment flow"""

from django.views.generic.edit import FormView
from experiments.forms import ParticipantForm
from django.core.exceptions import ObjectDoesNotExist


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
        experiment = self.__experiment_from_participant(participant)
        self.success_url += '%d/%d/' % (participant.id, experiment.id)
        return super(StartFlow, self).form_valid(form)

    def __experiment_from_participant(self, participant):
        latin_square_row = participant.row_participant

        try:
            latin_square = latin_square_row.row1_latin_square
        except ObjectDoesNotExist:
            latin_square = latin_square_row.row2_latin_square

        return latin_square.experiment
