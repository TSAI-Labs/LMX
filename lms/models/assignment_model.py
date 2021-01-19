# Core Django imports.
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

from lms.models.course_model import Course, StudentCourse
from lms.models.user_role_model import Role


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

    def clean(self):
        role = Role.objects.filter(user=self.created_by)
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


class StudentAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentassignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
