from django.db import models

from notario import settings
from accounts.models import Notary, Client

class Event(models.Model):
    
    APPOINTMENT = 'AP'
    DEADLINE = 'DL'
    OTHER = 'OT'
    CHOICES = [
        (APPOINTMENT, 'Appointment'),
        (DEADLINE, 'Deadline'),
        (OTHER, 'Other'),
    ]
    
    notary = models.ForeignKey(Notary, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=280)

    begin = models.DateTimeField()
    end = models.DateTimeField(null=True)

    event_type = models.CharField(
        max_length=2,
        choices=CHOICES,
        default=OTHER
    )