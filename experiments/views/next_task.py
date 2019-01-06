# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from experiments.models import Task

class NextTask(TemplateView):
    template_name = 'next_task.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NextTask, self).get_context_data(**kwargs)
        # Add the next task
        context['task'] = Task.objects.get(pk=13)
        return context
