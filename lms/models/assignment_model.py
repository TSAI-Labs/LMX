# Core Django imports.
from django.contrib.auth.models import User
from django.db import models
from lms.models.course_model import Course


class Assignment(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    for_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    max_grade = models.IntegerField()

    def __str__(self):
        return f'{self.name}'
