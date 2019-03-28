# -*- coding: utf-8 -*-
from datetime import datetime
from django.forms.models import model_to_dict
from django.views.generic import View
from django.http import HttpResponse
from experiments.models import Execution
import json

class IncrementNumberOfErrors(View):
    template_name= None
    def post(self, request, *args, **kwargs):
        number_of_errors = self.increment_number_of_errors(int(kwargs['execution_id']))
        response_kwargs = { 'content_type': 'application/json' }
        # import code; code.interact(local=dict(globals(), **locals()))
        result = { 'number_of_errors': number_of_errors }
        return HttpResponse(json.dumps(result), **response_kwargs)

    def increment_number_of_errors(self, execution_id):
        execution = Execution.objects.get(pk=execution_id)
        execution.number_of_errors += 1
        execution.save()
        execution.refresh_from_db()

        return execution.number_of_errors
