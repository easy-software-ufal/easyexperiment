# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from experiments.models import Task
from experiments.services.next_task_service import NextTaskService


class ViewTask(TemplateView):
    template_name = 'view_task.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ViewTask, self).get_context_data(**kwargs)

        task = Task.objects.get(pk=self.kwargs['task_id'])
        context['task'] = task

        return context
