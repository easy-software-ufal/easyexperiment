from datetime import timedelta
from experiments.models import Point, Execution


participants_ids = [54,71,4,34,41,52,43,32,10,45,38,79,6,81,77,36,30,49,60,47,66,13,18,64,2,62,75,56,73,58,8]
executions = Execution.objects.filter(participant_id__in=participants_ids)

for execution in executions:
    if (execution.start is None) or (execution.end is None):
        print("Execution %d has no start %s or end %s" % (execution.id, execution.start, execution.end,))
        continue
    start_time = execution.start + timedelta(hours=3)
    end_time = execution.end + timedelta(hours=3)
    points_number = Point.objects.filter(datetime__range=(start_time, end_time)).count()
    print("Execution %d: Participant: %d %d points" % (execution.id, execution.participant_id, points_number))
