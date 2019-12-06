# -*- coding: utf-8 -*-

from django import forms

from experiments.models import Execution, Experiment, HeatMapFeedback,\
    LatinSquare, Participant
from experiments.services.search_available_latin_square_row import \
    SearchAvailableLatinSquareRow


class ParticipantForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(
        help_text='A valid email address, please.', required=False
    )
    experiment_id = forms.IntegerField(
        widget=forms.HiddenInput(), required=True
    )

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

    def save_participant(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        experiment_id = self.cleaned_data['experiment_id']
        experiment = self.__experiment(experiment_id)

        participant = Participant.objects.create(name=name, email=email)

        latin_square_row = SearchAvailableLatinSquareRow(experiment).call()

        if latin_square_row is not None:
            latin_square_row.participant = participant
            latin_square_row.save()
        else:
            latin_square = LatinSquare.objects.create_with_rows(
                experiment=experiment)
            latin_square.row1.participant = participant
            latin_square.row1.save()

        return participant

    def __experiment(self, experiment_id):
        return Experiment.objects.get(pk=experiment_id)


class HeatMapFeedbackForm(forms.Form):
    execution_id = forms.IntegerField(
        widget=forms.HiddenInput(), required=True)
    corresponds_to_perception = forms.BooleanField(
        label='O gráfico ao lado exibe as áreas da função para onde você precisou olhar com mais frequência para entender o código. Você concorda com ele?',
        initial=False, required=False)
    notes = forms.CharField(
        label='Gostaria de deixar algum comentário?',
        max_length=500, widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(HeatMapFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['notes'].widget.attrs['class'] = 'form-control'

    def save_heat_map_feedback(self):
        corresponds_to_perception = self.cleaned_data[
            'corresponds_to_perception'
        ]
        notes = self.cleaned_data['notes']
        execution_id = self.cleaned_data['execution_id']
        execution = self.__execution(execution_id)

        return HeatMapFeedback.objects.create(
            corresponds_to_perception=corresponds_to_perception,
            notes=notes,
            execution=execution
        )

    def __execution(self, execution_id):
        return Execution.objects.get(pk=execution_id)
