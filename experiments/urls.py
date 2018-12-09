from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^choose_flow/$', views.flow_choice_screen),
    url(r'^start_flow/(?P<flow_number>[0-9]+)/$', views.start_flow, name="start_flow"),
    url(r'^create_participant/(?P<flow_number>[0-9]+)/$', views.create_participant, name="create_participant"),
    url(r'^second_task/(?P<participant_id>[0-9]+)/(?P<flow_number>[0-9]+)/$', views.second_task, name="second_task"),
    url(r'^finish/(?P<participant_id>[0-9]+)/$', views.finish, name="finish"),
]