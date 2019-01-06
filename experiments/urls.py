# -*- coding: utf-8 -*-
from django.conf.urls import url

# from . import views

from experiments.views.choose_experiment import ExperimentList
from experiments.views.next_task import NextTask
from experiments.views.start_flow import StartFlow

urlpatterns = [
    url(r'^$', ExperimentList.as_view(), name='choose_experiment'),
    url(r'^start-flow/(?P<experiment_id>[0-9]+)/$', StartFlow.as_view(), name='start_flow'),
    url(r'^next-task/$', NextTask.as_view(), name='next_task'),
    # url(r'^choose_flow/$', views.flow_choice_screen),
    # url(r'^start_flow/(?P<flow_number>[0-9]+)/$', views.start_flow, name="start_flow"),
    # url(r'^create_participant/(?P<flow_number>[0-9]+)/$', views.create_participant, name="create_participant"),
    # url(r'^second_task/(?P<participant_id>[0-9]+)/(?P<flow_number>[0-9]+)/$', views.second_task, name="second_task"),
    # url(r'^finish/(?P<participant_id>[0-9]+)/$', views.finish, name="finish"),
]
