# Core Django imports.
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django import forms
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from image_optimizer.fields import OptimizedImageField

import os

from lms.models.course_model import Course, StudentCourse
from lms.models.user_role_model import Role


def upload_path(instance, filename):
    # change the filename here is required
    return os.path.join(instance.name, filename)

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

    name = models.CharField(max_length=30)
    description = RichTextUploadingField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    for_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    display_grades = models.CharField(choices=GRADES_DISPLAY, max_length=20, default='percentage')
    sub_type = models.CharField(choices=SUBMISSION_TYPE, max_length=20, default='no submission')

    max_grade = models.IntegerField()

    image = OptimizedImageField(
        upload_to=upload_path,
        optimized_image_output_size=(900, 900),
        optimized_image_resize_method='cover',  # 'thumbnail', 'cover' or None
        null=True,
        blank=True
        )

    def __str__(self):
        return f'{self.name}'

    def clean(self):
        role = Role.objects.filter(user=self.created_by)
        print('***********RRRRRRRROLLLLLLLLLEEEEEEE*********',role)
        if role:
            if not (role[0].is_admin or role[0].is_teacher):
                raise ValidationError("Only Teacher Or Admin Can Create Assignment")
            if not self.for_course.user == self.created_by:
                raise ValidationError("Teacher of this course only can create assignments")
        else:
            
            raise ValidationError("Assign Role to the User")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        students = StudentCourse.objects.filter(courses=self.for_course)
        for student in students:
            if student.registered:
                temp_object = StudentAssignment(user=student.user, assignment=self)
                temp_object.save()
    

# Comment Model - Seperate from teacher and student model's
class Comment(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete = models.CASCADE,related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length = 200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
    class Meta:
        ordering = ['-date']

class StudentAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentassignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)



