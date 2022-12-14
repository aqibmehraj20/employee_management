from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class Employees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_email = models.EmailField()
    job_position = models.CharField(max_length=250, blank=False, null=False)
    is_hr = models.BooleanField(blank=True, null=True)
    is_manager = models.BooleanField(blank=True, null=True)
    hiring_date = models.DateField(max_length=250, null=False, blank=False)
    description = models.TextField(max_length=255, null=True, blank=True);

    def __str__(self):
        return "{}".format(self.user)


leaveStatus_CHOICE = (
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
)


class LeavesRequest(models.Model):
    user = models.ForeignKey(Employees, on_delete=models.CASCADE, blank=True, null=True)
    duration_from = models.DateTimeField(default=timezone.now)
    duration_to = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=500, choices=leaveStatus_CHOICE, default='Pending')

    def __str__(self):
        return "{}".format(self.user)
