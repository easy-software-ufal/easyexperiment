# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from experiments.models import Participant, Experiment


class PreviousTask(TemplateView):
    template_name = 'next_task.html'

    def __init__(self, **kwargs):
        super(PreviousTask, self).__init__(**kwargs)
        self.execution = None

    def get(self, request, *args, **kwargs):
        participant = self.__get_participant(kwargs['participant_id'])

        participant.finish_all_pauses()

        self.execution = participant.execution_set.all().latest('created_at')

        return super(PreviousTask, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PreviousTask, self).get_context_data(**kwargs)

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
