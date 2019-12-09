# -*- coding: utf-8 -*-
import json

from django.db.models import F
from django.http import HttpResponse
from django.views.generic import View

from experiments.models import Execution, Answer


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


class SubmitAnswer(View):
    template_name = None

    def post(self, request, *args, **kwargs):
        response_kwargs = {'content_type': 'application/json'}

        answer = self.create_new_answer()

        return HttpResponse(json.dumps({'correct': answer.correct}, default=date_handler), **response_kwargs)

    def create_new_answer(self):
        user_answer = self.request.POST.get('answer')
        execution = self.__execution()
        correct = execution.task.correct_answer == user_answer.strip()
        execution_id = self.__execution_id()
        if not correct: self.increment_number_of_errors(execution_id)

        return Answer.objects.create(execution_id=execution_id, answer=user_answer, correct=correct)

    def increment_number_of_errors(self):
        Execution.objects.filter(pk=self.__execution_id()).update(number_of_errors=F('number_of_errors') + 1)

        execution = Execution.objects.get(pk=self.__execution_id())
        return execution.number_of_errors

    def __execution_id(self):
        try:
            return self.execution_id
        except AttributeError:
            self.execution_id = int(self.kwargs['execution_id'])
            return self.execution_id

    def __execution(self):
        return Execution.objects.get(pk=self.__execution_id())
