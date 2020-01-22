# -*- coding: utf-8 -*-
"""First screen of experiment flow"""

from django.views.generic.edit import FormView
from experiments.forms import ParticipantForm
from django.core.exceptions import ObjectDoesNotExist


class StartFlow(FormView):
    template_name = 'start_flow.html'
    form_class = ParticipantForm
    success_url = '/experiments/social-representation/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(StartFlow, self).get_initial()

        initial['experiment_id'] = self.kwargs['experiment_id']

        return initial

    def form_valid(self, form):
        participant = form.save_participant()
        self.success_url += '%d/' % participant.id
        return super(StartFlow, self).form_valid(form)
