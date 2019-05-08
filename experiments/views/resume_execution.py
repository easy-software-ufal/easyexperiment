# -*- coding: utf-8 -*-
from datetime import datetime
from django.forms.models import model_to_dict
from django.views.generic import View
from django.http import HttpResponse
from experiments.models import Pause
import json

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

class ResumeExecution(View):
    template_name = None
    def post(self, request, *args, **kwargs):
        pause = self.get_last_pause_for_execution(int(kwargs['execution_id']))
        pause.end_time = datetime.now()
        pause.save()
        response_kwargs = { 'content_type': 'application/json' }
        pause.refresh_from_db()
        return HttpResponse(json.dumps(model_to_dict(pause), default=date_handler), **response_kwargs)

    def get_last_pause_for_execution(self, execution_id):
        return Pause.objects.filter(execution_id=execution_id).order_by('-pk')[0]
