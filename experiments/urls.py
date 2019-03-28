# -*- coding: utf-8 -*-
from django.conf.urls import url

# from . import views

from experiments.views.choose_experiment import ExperimentList
from experiments.views.finish_execution import FinishExecution
from experiments.views.increment_number_of_errors import IncrementNumberOfErrors
from experiments.views.pause_execution import PauseExecution
from experiments.views.resume_execution import ResumeExecution
from experiments.views.next_task import NextTask
from experiments.views.start_flow import StartFlow

urlpatterns = [
    url(r'^$', ExperimentList.as_view(), name='choose_experiment'),
    url(r'^start-flow/(?P<experiment_id>[0-9]+)/$', StartFlow.as_view(), name='start_flow'),
    url(r'^next-task/(?P<participant_id>[0-9]+)/(?P<experiment_id>[0-9]+)/$', NextTask.as_view(), name='next_task'),
    url(r'^finish-execution/$', FinishExecution.as_view(), name='finish_execution'),
    url(r'^pause-execution/(?P<execution_id>[0-9]+)/$', PauseExecution.as_view(), name='pause_execution'),
    url(r'^resume-execution/(?P<execution_id>[0-9]+)/$', ResumeExecution.as_view(), name='resume_execution'),
    url(r'^increment-number-of-errors/(?P<execution_id>[0-9]+)/$', IncrementNumberOfErrors.as_view(), name='increment_number_of_errors'),

]
