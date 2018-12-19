# -*- coding: utf-8 -*-
from django.views.generic.list import View
from experiments.models import Experiment

class ExperimentList(View):
    model = Experiment
    paginate_by = 100
