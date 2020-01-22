# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from experiments.forms import DifficultLinesFeedbackForm
from experiments.models import Execution

class DifficultLinesView(FormView):
    template_name = 'difficult_lines.html'
    form_class = DifficultLinesFeedbackForm
    success_url = '/experiments/difficult-lines/'

    def get_context_data(self):
        context = super(DifficultLinesView, self).get_context_data()

        execution_id = self.kwargs['execution_id']
        execution = Execution.objects.get(pk=execution_id)

        context['execution'] = execution

        return context

    def next_execution(self, execution):
        participant_id = execution.participant.id

        return Execution.objects.order_by('id').filter(
            participant__id=participant_id,
            id__gt=execution.id
        ).first()


    def first_execution(self, participant):
        return Execution.objects.order_by('id').filter(participant__id=participant.id).first().id


    def form_valid(self, form):
        difficult_lines_feedback = form.save_difficult_lines_feedback()
        next_execution = self.next_execution(difficult_lines_feedback.execution)

        if next_execution is None:
            first_execution = self.first_execution(difficult_lines_feedback.execution.participant)
            self.success_url = "/experiments/heat-map/%d/" % first_execution
        else:
            self.success_url = "/experiments/difficult-lines/%d/" % next_execution.id

        return super(DifficultLinesView, self).form_valid(form)

