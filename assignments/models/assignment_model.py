from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from lms.models.course_model import Course
from django import forms


class Assignment(models.Model):
    GRADES_DISPLAY = (
        ('percentage', 'Percentage'),
        ('complete/Incomplete', 'Complete/Incomplete'),
        ('points', 'Points'),
        ('letter grade', 'Letter Grade'),
        ('GPA scale', 'GPA Scale'),
        ('not graded', 'Not Graded')
    )

    SUBMISSION_TYPE = (
        ('no submission', 'No  Submission'),
        ('online', 'Online'),
        ('on paper', 'On Paper'),
        ('external tool', 'External Tool')
    )

    title = models.CharField(max_length=100)
    # content = models.TextField()
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(blank=True, null=True, default=0)
    display_grades = models.CharField(choices=GRADES_DISPLAY, max_length=20, default='percentage')
    sub_type = models.CharField(choices=SUBMISSION_TYPE, max_length=20, default='no submission')
    anonymous_grading = models.BooleanField(default=False)
    assign_to = models.ManyToManyField(Course, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    available_from = models.DateField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)
    # image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)

    # teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    # course

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lms:assignment_detail', args=(str(self.id)))


class Comment(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete = models.CASCADE,related_name="comments")
    author = models.CharField(max_length = 50)
    content = models.TextField(max_length = 200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
    class Meta:
        ordering = ['-date']