# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from experiments.models import Participant, Experiment, Execution, Task
from experiments.services.next_task_service import NextTaskService


class NextTask(TemplateView):
    template_name = 'next_task.html'

    def get(self, request, *args, **kwargs):
        experiment = self.__get_experiment(kwargs['experiment_id'])
        participant = self.__get_participant(kwargs['participant_id'])

        if 'previous_execution_id' in self.request.GET:
            execution = Execution.objects.get(pk=self.request.GET.get('previous_execution_id'))
            execution.end = datetime.now()
            execution.save()

        task = NextTaskService(experiment, participant).call()

        if task is None:
            # TODO: create an 'end' view and substitute here
            return HttpResponseRedirect('/experiments/finish-execution/')

        self.__create_execution(participant, task)

        return super(NextTask, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NextTask, self).get_context_data(**kwargs)

        # load experiment and participant
        experiment = self.__get_experiment(self.kwargs['experiment_id'])
        participant = self.__get_participant(self.kwargs['participant_id'])

        context['experiment_id'] = experiment.id
        context['participant_id'] = participant.id
        context['execution'] = self.execution

        return context

    def __get_experiment(self, experiment_id):
        if not hasattr(self, 'experiment'):
            self.experiment = Experiment.objects.get(pk=experiment_id)

        return self.experiment

    def __get_participant(self, participant_id):
        if not hasattr(self, 'participant'):
            self.participant = Participant.objects.get(pk=participant_id)

        return self.participant

    def __create_execution(self, participant, task):
        self.execution = Execution.objects.create(participant = participant, task = task, start = datetime.now())
