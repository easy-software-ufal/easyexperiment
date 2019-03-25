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

class PauseExecution(View):
    template_name= None
    def post(self, request, *args, **kwargs):
        pause = self.create_pause(int(kwargs['execution_id']))
        response_kwargs = { 'content_type': 'application/json' }
        # import code; code.interact(local=dict(globals(), **locals()))
        pause.refresh_from_db()
        return HttpResponse(json.dumps(model_to_dict(pause), default=date_handler), **response_kwargs)

    def create_pause(self, execution_id):
        return Pause.objects.create(execution_id=execution_id, start_time=datetime.now())
