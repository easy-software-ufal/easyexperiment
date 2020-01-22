# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from experiments.models import Experiment

class ExperimentList(ListView):
    model = Experiment
    paginate_by = 100

    def get_queryset(self):
        return Experiment.objects.filter(hidden=False)
