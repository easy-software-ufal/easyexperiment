# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from experiments.models import Participant, Execution, Task
from experiments.services.next_task_service import NextTaskService


class NextTask(TemplateView):
    template_name = 'next_task.html'

    def get(self, request, *args, **kwargs):
        participant = self.__get_participant(kwargs['participant_id'])

        participant.finish_last_pause_for_each_execution()

        if 'previous_execution_id' in self.request.GET:
            execution = Execution.objects.get(pk=self.request.GET.get('previous_execution_id'))
            execution.end = datetime.now()
            execution.save()

        task = NextTaskService(participant).call()

        if task is None:
            # TODO: create an 'end' view and substitute here
            first_execution = self.first_execution(participant)
            return HttpResponseRedirect("/experiments/difficult-lines/%d/" % first_execution)

        self.__create_execution(participant, task)

        return super(NextTask, self).get(request, args, kwargs)

    def first_execution(self, participant):
        return Execution.objects.order_by('id').filter(participant__id=participant.id).first().id


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NextTask, self).get_context_data(**kwargs)

        # load experiment and participant
        participant = self.__get_participant(self.kwargs['participant_id'])
        experiment = participant.experiment

        context['experiment_id'] = experiment.id
        context['participant_id'] = participant.id
        context['execution'] = self.execution

        return context


    def __get_participant(self, participant_id):
        if not hasattr(self, 'participant'):
            self.participant = Participant.objects.get(pk=participant_id)

        return self.participant

    def __create_execution(self, participant, task):
        self.execution = Execution.objects.create(participant = participant, task = task, start = datetime.now())
