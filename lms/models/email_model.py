# Core Django imports.
from django.contrib.auth.models import User
from django.db import models

class Email(models.Model):
    student = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'emails')
    subject = models.CharField(max_length = 250, null = False, blank = False, unique = True)
    emailBody = models.CharField(max_length = 1000, null = False, blank = False, unique = True)