from django.views.generic.edit import FormView
from experiments.forms import SocialRepresentationForm
from experiments.models import SocialRepresentation

class SocialRepresentationView(FormView):
    template_name = 'social_representation.html'
    form_class = SocialRepresentationForm
    success_url = '/experiments/next-task/'

    def get_context_data(self):
        context = super(SocialRepresentationView, self).get_context_data()

        context['participant_id'] = self.kwargs['participant_id']

        return context

    def form_valid(self, form):
        social_representation = form.save_social_representation()

        participant = social_representation.participant

        self.success_url += '%d/' % participant.id
        return super(SocialRepresentationView, self).form_valid(form)

