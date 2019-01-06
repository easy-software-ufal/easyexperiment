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
        form.save_participant()
        return super(StartFlow, self).form_valid(form)
