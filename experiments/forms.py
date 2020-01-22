# -*- coding: utf-8 -*-

from django import forms

from experiments.models import Execution, Experiment, HeatMapFeedback,\
    LatinSquare, Participant, SocialRepresentation, DifficultLinesFeedback
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

        participant = Participant.objects.create(name=name, email=email, experiment=experiment)

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


class DifficultLinesFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DifficultLinesFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['hard_lines'].widget.attrs['class'] = 'form-control'

    def save_difficult_lines_feedback(self):
        hard_lines = self.cleaned_data['hard_lines']
        execution_id = self.data['execution_id']
        return DifficultLinesFeedback.objects.create(
            hard_lines=hard_lines,
            execution_id=execution_id
        )

    class Meta:
        model = DifficultLinesFeedback
        fields = ['hard_lines']



class SocialRepresentationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SocialRepresentationForm, self).__init__(*args, **kwargs)
        self.fields['words'].widget.attrs['class'] = 'form-control'
        self.fields['most_relevant'].widget.attrs['class'] = 'form-control'


    class Meta:
        model = SocialRepresentation
        fields = ['words', 'most_relevant']

    def save_social_representation(self):
        words = self.cleaned_data['words']
        most_relevant = self.cleaned_data['most_relevant']
        participant_id = self.data['participant_id']
        participant = self.__participant(participant_id)

        return SocialRepresentation.objects.create(
            words = words,
            most_relevant = most_relevant,
            participant = participant
        )

    def __participant(self, participant_id):
        return Participant.objects.get(pk=participant_id)
