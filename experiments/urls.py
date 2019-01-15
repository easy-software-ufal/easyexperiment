# -*- coding: utf-8 -*-
from django.conf.urls import url

# from . import views

from experiments.views.choose_experiment import ExperimentList
from experiments.views.finish_execution import FinishExecution
from experiments.views.next_task import NextTask
from experiments.views.start_flow import StartFlow

urlpatterns = [
    url(r'^$', ExperimentList.as_view(), name='choose_experiment'),
    url(r'^start-flow/(?P<experiment_id>[0-9]+)/$', StartFlow.as_view(), name='start_flow'),
    url(r'^next-task/(?P<participant_id>[0-9]+)/(?P<experiment_id>[0-9]+)/$', NextTask.as_view(), name='next_task'),
    url(r'^finish-execution/$', FinishExecution.as_view(), name='finish_execution'),
]
