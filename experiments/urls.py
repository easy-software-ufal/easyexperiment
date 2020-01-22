# -*- coding: utf-8 -*-
from django.conf.urls import url

# from . import views

from experiments.views.choose_experiment import ExperimentList
from experiments.views.finish_execution import FinishExecution
from experiments.views.heat_map import HeatMap
from experiments.views.increment_number_of_errors import IncrementNumberOfErrors
from experiments.views.pause_execution import PauseExecution
from experiments.views.previous_task import PreviousTask
from experiments.views.resume_execution import ResumeExecution
from experiments.views.next_task import NextTask
from experiments.views.start_flow import StartFlow
from experiments.views.submit_answer import SubmitAnswer
from experiments.views.social_representation import SocialRepresentationView
from experiments.views.difficult_lines import DifficultLinesView


urlpatterns = [
    url(r'^$', ExperimentList.as_view(), name='choose_experiment'),
    url(r'^start-flow/(?P<experiment_id>[0-9]+)/$', StartFlow.as_view(), name='start_flow'),
    url(r'^next-task/(?P<participant_id>[0-9]+)/$', NextTask.as_view(), name='next_task'),
    url(r'^previous-task/(?P<participant_id>[0-9]+)/(?P<experiment_id>[0-9]+)/$', PreviousTask.as_view(), name='previous_task'),
    url(r'^finish-execution/$', FinishExecution.as_view(), name='finish_execution'),
    url(r'^pause-execution/(?P<execution_id>[0-9]+)/$', PauseExecution.as_view(), name='pause_execution'),
    url(r'^resume-execution/(?P<execution_id>[0-9]+)/$', ResumeExecution.as_view(), name='resume_execution'),
    url(r'^increment-number-of-errors/(?P<execution_id>[0-9]+)/$', IncrementNumberOfErrors.as_view(), name='increment_number_of_errors'),
    url(r'^submit-answer/(?P<execution_id>[0-9]+)/$', SubmitAnswer.as_view(), name='submit_answer'),
    url(r'^heat-map/(?P<execution_id>[0-9]+)/$', HeatMap.as_view(), name='heat_map'),
    url(r'^social-representation/(?P<participant_id>[0-9]+)/$', SocialRepresentationView.as_view(), name='social_representation'),
    url(r'^difficult-lines/(?P<execution_id>[0-9]+)/?', DifficultLinesView.as_view(), name='difficult_lines'),
]
