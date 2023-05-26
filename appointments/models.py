import datetime
from uuid import uuid4
from django.db import models
from django.utils import timezone

from authentication.models import User

# Create your models here.

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.TextField('Appointment title')
    start = models.DateTimeField('Appointment start time', default=datetime.datetime.now())
    end = models.DateTimeField('Appointment end time', default=datetime.datetime.now())
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    patient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')