# Core Django imports.
from django.contrib.auth.models import User
from django.db import models

class Course(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=250, null=False, blank=False, unique=True)

