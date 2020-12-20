from django.views.generic.edit import FormView
from experiments.forms import HeatMapFeedbackForm
from experiments.models import Execution, Point

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pygazeanalyser.gazeplotter import draw_heatmap

import numpy
import os
import time
from datetime import datetime

# DIRECTORIES
# paths
DIR = os.path.dirname(__file__)
PLOTDIR = os.path.join(
    DIR, '..', '..', 'media', 'uploads', 'executions', 'heatmaps'
)
IMGDIR = os.path.join(DIR, '..', '..', 'uploads')

# check if output directories exist; if not, create it
if not os.path.isdir(PLOTDIR):
    os.mkdir(PLOTDIR)

# EXPERIMENT SPECS
DISPSIZE = (1920, 1080)  # (px,px)
SCREENSIZE = (39.9, 29.9)  # (cm,cm)
SCREENDIST = 61.0  # cm
PXPERCM = numpy.mean([DISPSIZE[0] / SCREENSIZE[0], DISPSIZE[1] / SCREENSIZE[1]])  # px/cm


def c_time():
    return "\033[94m %s \033[0m" % datetime.now().ctime()


class HeatMap(FormView):
    template_name = 'heat_map.html'
    form_class = HeatMapFeedbackForm
    success_url = '/experiments/heat-map/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(HeatMap, self).get_initial()
        initial['execution_id'] = self.kwargs['execution_id']
        # execution = self.__execution(245)
        execution = self.__execution(self.kwargs['execution_id'])

        if not execution.end:
            execution.end = datetime.now()
            execution.save()

        if not execution.heatmap:
            self.__generate_heat_map(execution)

        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HeatMap, self).get_context_data(**kwargs)

        # load execution
        execution = Execution.objects.get(pk=self.kwargs['execution_id'])
        context['execution_heatmap_url'] = execution.heatmap.url

        return context

    def __generate_heat_map(self, execution):
        background_image = DIR + "/../.." + execution.task.image.url

        points = Point.objects.filter(
            datetime__range=(execution.start, execution.end)
        )

        # exclude pause points
        for pause in execution.pause_set.all():
            points = points.exclude(datetime__range=(pause.start_time, pause.end_time))

        # NEW OUTPUT DIRECTORIES
        # create a new output directory for the current participant
        pplotdir = os.path.join(PLOTDIR, str(execution.id))

        # check if the directory already exists
        if not os.path.isdir(pplotdir):
            # create it if it doesn't yet exist
            os.mkdir(pplotdir)

        # # # # #
        # PLOTS

        print("%s: Plotting gaze data" % c_time())
        fixations = []
        x_points = []
        y_points = []
        # imagefile = execution.task.image # os.path.join(DIR, '..', '..', 'uploads', 'tasks', background_image)
        imagefile = background_image
        heatmap_file = os.path.join(pplotdir, 'heatmap')

        for point in points:
            x = int(float(point.x.replace(',', '.')))
            y = int(float(point.y.replace(',', '.')))

            x_points.append(x)
            y_points.append(y)

            fixations.append([time.time(), time.time(), int(1), x, y])

        print("%s: Generating Heat Map" % c_time())
        draw_heatmap(fixations, DISPSIZE, imagefile=imagefile,
                     durationweight=True, alpha=0.5,
                     savefilename=heatmap_file)

        # Save image path on execution
        execution.heatmap = 'uploads/executions/heatmaps/{0}/heatmap.png'.format(execution.id)
        print(execution.heatmap)
        execution.save()
        return execution.heatmap.url

    def __execution(self, execution_id):
        return Execution.objects.get(pk=execution_id)

    def next_execution(self, execution):
        participant_id = execution.participant.id

        return Execution.objects.order_by('id').filter(
            participant__id=participant_id,
            id__gt=execution.id
        ).first()

    def form_valid(self, form):
        heat_map_feedback = form.save_heat_map_feedback()

        next_execution = self.next_execution(heat_map_feedback.execution)

        if next_execution is None:
            self.success_url = '/experiments/finish-execution/'
        else:
            self.success_url += "%d/" % next_execution.id

        # self.success_url += '%d/%d/?previous_execution_id=%s' % (
        #     participant.id, experiment.id, heat_map_feedback.execution.id)
        return super(HeatMap, self).form_valid(form)
