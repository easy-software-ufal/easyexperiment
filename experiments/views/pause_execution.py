# -*- coding: utf-8 -*-
from datetime import datetime

from django.views.generic import TemplateView

from experiments.models import Pause, Execution


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


class PauseExecution(TemplateView):
    template_name = 'pause_execution.html'

    def get(self, request, *args, **kwargs):
        # finish previous pauses, this is needed in case of user refresh the screen
        execution = Execution.objects.get(pk=kwargs['execution_id'])
        execution.participant.finish_last_pause_for_each_execution()

        return super(PauseExecution, self).get(request, args, kwargs)

    def create_pause(self, execution_id):
        return Pause.objects.create(execution_id=execution_id, start_time=datetime.now())

    def get_context_data(self):
        # Call the base implementation
        context = super(PauseExecution, self).get_context_data()
        # import code;
        # code.interact(local=dict(globals(), **locals()))

        pause = self.create_pause(int(self.kwargs['execution_id']))

        context['pause'] = pause

        return context
