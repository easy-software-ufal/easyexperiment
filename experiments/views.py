# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render
from experiments.models import Participant

def flow_choice_screen(request):
    return render(request, 'experiments/choose_flow.html')

def start_flow(request, flow_number):
    context = {'flow_number': flow_number}
    return render(request, 'experiments/create_participant.html', context)

def create_participant(request, flow_number):
    name = request.POST.get('name')
    email = request.POST.get('email')
    participant = Participant.objects.create(name = name, email = email, flow = flow_number, start_datetime = datetime.now(), task1_start = datetime.now())

    clear_gaze_data_file()

    context = { 'participant_id': participant.id, 'flow_number': flow_number}
    return render(request, "experiments/flow%s_task1.html" % flow_number, context)

def second_task(request, participant_id, flow_number):
    data = read_gaze_data_file()
    Participant.objects.filter(pk=participant_id).update(task1_end = datetime.now(), task1_data = data, task2_start = datetime.now())
    clear_gaze_data_file()
    context = { 'participant_id': participant_id, 'flow_number': flow_number}
    return render(request, "experiments/flow%s_task2.html" % flow_number, context)

def finish(request, participant_id):
    data = read_gaze_data_file()
    Participant.objects.filter(pk=participant_id).update(end_datetime=datetime.now(), task2_end = datetime.now(), task2_data = data)
    clear_gaze_data_file()
    return render(request, "experiments/finish.html")


GAZE_DATA_FILE = 'c:\\users\\nando\\desktop\\gaze_data.txt'
# utils
def clear_gaze_data_file():
    open(GAZE_DATA_FILE, 'w').close()

def read_gaze_data_file():
    with open(GAZE_DATA_FILE, 'r') as filehandle:  
        return filehandle.readlines()
